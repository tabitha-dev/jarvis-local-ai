"""Public voice-selection guardrails. No models or voices are downloaded here."""
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import voice_settings
import select_voice
import jarvis


class VoiceSettingsTests(unittest.TestCase):
    def test_public_options_strict_and_alan_excluded(self):
        self.assertEqual(set(voice_settings.VOICE_MODELS),
                         {"windows", "piper:en_GB-cori-medium"})
        self.assertFalse(any('alan' in v.lower() for v in voice_settings.VOICE_MODELS))
        source = (Path(jarvis.__file__).parent / 'setup.bat').read_text(encoding='utf-8').lower()
        self.assertNotIn('alan', source)
        self.assertNotIn('set /p', source)
        self.assertIn('tools\\select_voice.py', source)

    def test_default_when_config_missing_corrupt_or_unknown(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'commands.json'
            self.assertEqual(voice_settings.get_voice(p), 'windows')
            p.write_text('{not json', encoding='utf-8')
            self.assertEqual(voice_settings.get_voice(p), 'windows')
            p.write_text('{"voice":"piper:en_GB-alan-medium"}', encoding='utf-8')
            self.assertEqual(voice_settings.get_voice(p), 'windows')
            p.write_text('{"voice":["windows"]}', encoding='utf-8')
            self.assertEqual(voice_settings.get_voice(p), 'windows')
            p.write_text('{"voice":"piper:en_GB-cori-medium"}', encoding='utf-8')
            self.assertEqual(voice_settings.get_voice(p), 'piper:en_GB-cori-medium')

    def test_saving_selection_preserves_other_private_shortcuts(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'commands.json'
            p.write_text(json.dumps({'apps': {'notes':'notepad'}, 'voice': 'windows'}), encoding='utf-8')
            voice_settings.save_voice('piper:en_GB-cori-medium', p)
            self.assertEqual(json.loads(p.read_text())['apps'], {'notes':'notepad'})
            self.assertEqual(voice_settings.get_voice(p), 'piper:en_GB-cori-medium')
            self.assertFalse(list(Path(d).glob('.voice-setting-*')))
            with self.assertRaises(ValueError):
                voice_settings.save_voice('piper:en_GB-alan-medium', p)
            self.assertEqual(voice_settings.get_voice(p), 'piper:en_GB-cori-medium')

    def test_corrupted_existing_config_not_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'commands.json'
            p.write_text('not-json', encoding='utf-8')
            with self.assertRaises(ValueError):
                voice_settings.save_voice('windows', p)
            self.assertEqual(p.read_text(), 'not-json')


class VoiceMenuTests(unittest.TestCase):
    def test_unattended_non_windows_defaults_to_windows(self):
        self.assertEqual(select_voice.choose_menu(timeout=0), 'windows')

    def test_menu_accepts_only_two_numbered_options(self):
        self.assertEqual(select_voice.NUMBERED, {'1':'windows','2':'piper:en_GB-cori-medium'})
        with self.assertRaises(ValueError):
            select_voice.apply_voice('piper:en_GB-alan-medium')

    def test_windows_does_not_trigger_download(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(select_voice.subprocess, 'run') as run:
            select_voice.apply_voice('windows', config=Path(d)/'commands.json')
            run.assert_not_called()
            self.assertEqual(voice_settings.get_voice(Path(d)/'commands.json'), 'windows')

    def test_cori_download_uses_fixed_argument_list(self):
        with tempfile.TemporaryDirectory() as d, \
             mock.patch.object(select_voice.subprocess,'run') as run:
            p=Path(d)/'commands.json'
            select_voice.apply_voice('piper:en_GB-cori-medium', config=p, python_exe='python-test')
            argv=run.call_args.args[0]
            self.assertEqual(argv[:4], ['python-test','-m','piper.download_voices','en_GB-cori-medium'])
            self.assertTrue(run.call_args.kwargs['check'])
            self.assertEqual(voice_settings.get_voice(p),'piper:en_GB-cori-medium')

    def test_failed_download_does_not_overwrite_config(self):
        import subprocess
        with tempfile.TemporaryDirectory() as d, \
             mock.patch.object(select_voice.subprocess, 'run', side_effect=subprocess.CalledProcessError(1,'python')):
            p=Path(d)/'commands.json'
            voice_settings.save_voice('windows',p)
            with self.assertRaises(subprocess.CalledProcessError):
                select_voice.apply_voice('piper:en_GB-cori-medium',config=p)
            self.assertEqual(voice_settings.get_voice(p),'windows')

    def test_enter_and_keys_windows_console(self):
        fake_input=mock.Mock()
        fake_input.isatty.return_value=True
        for key,expected in [('\r','windows'),('1','windows'),('2','piper:en_GB-cori-medium')]:
            fake_console=types.SimpleNamespace(kbhit=lambda: True, getwch=lambda: key)
            with mock.patch.object(select_voice,'os',types.SimpleNamespace(name='nt')), \
                 mock.patch.object(select_voice.sys,'stdin',fake_input), \
                 mock.patch.dict(sys.modules,{'msvcrt':fake_console}):
                self.assertEqual(select_voice.choose_menu(timeout=0.5),expected)


class VoiceRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.pyttsx3 = mock.Mock()
        self.pyttsx3.init.return_value=mock.Mock()
        self.piper_class = mock.Mock()
        self.mod_patch=mock.patch.dict(sys.modules,{'pyttsx3':self.pyttsx3,'piper':types.SimpleNamespace(PiperVoice=self.piper_class)})
        self.mod_patch.start()
        self.addCleanup(self.mod_patch.stop)

    def test_windows_default_uses_windows_and_no_piper(self):
        with mock.patch.object(jarvis,'get_voice',return_value='windows'):
            voice=jarvis.Voice()
        self.assertIsNone(voice.piper)
        self.pyttsx3.init.assert_called_once()
        self.piper_class.load.assert_not_called()

    def test_cori_choice_loads_approved_voice(self):
        with tempfile.TemporaryDirectory() as d, \
             mock.patch.object(jarvis,'get_voice',return_value='piper:en_GB-cori-medium'), \
             mock.patch.object(jarvis,'VOICES_DIR',Path(d)):
            (Path(d)/'en_GB-cori-medium.onnx').write_bytes(b'test-only')
            voice=jarvis.Voice()
            self.assertIsNotNone(voice.piper)
            self.piper_class.load.assert_called_once_with(str(Path(d)/'en_GB-cori-medium.onnx'))
            self.pyttsx3.init.assert_not_called()

    def test_missing_selected_piper_falls_back(self):
        with tempfile.TemporaryDirectory() as d, \
             mock.patch.object(jarvis,'get_voice',return_value='piper:en_GB-cori-medium'), \
             mock.patch.object(jarvis,'VOICES_DIR',Path(d)):
            voice=jarvis.Voice()
            self.assertIsNone(voice.piper)
            self.pyttsx3.init.assert_called_once()

    def test_broken_piper_load_falls_back(self):
        self.piper_class.load.side_effect=RuntimeError('invalid model')
        with tempfile.TemporaryDirectory() as d, \
             mock.patch.object(jarvis,'get_voice',return_value='piper:en_GB-cori-medium'), \
             mock.patch.object(jarvis,'VOICES_DIR',Path(d)):
            (Path(d)/'en_GB-cori-medium.onnx').write_bytes(b'bad')
            voice=jarvis.Voice()
            self.assertIsNone(voice.piper)
            self.pyttsx3.init.assert_called_once()

if __name__=='__main__':
    unittest.main()
