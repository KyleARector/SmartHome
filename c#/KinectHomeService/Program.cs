using System;
using System.Collections.Generic;
using System.Windows.Forms;
using Microsoft.Kinect;
using Microsoft.Speech.AudioFormat;
using Microsoft.Speech.Recognition;
using System.IO;
using System.Net;

namespace KinectHomeService
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            using (ProcessIcon procIcon = new ProcessIcon())
            {
                procIcon.Display();
                KinectInterface kinect = new KinectInterface();
                Application.Run();
            }
        }
    }

    class KinectInterface
    {
        /// <summary>
        /// Active Kinect sensor.
        /// </summary>
        private KinectSensor sensor;

        /// <summary>
        /// Speech recognition engine using audio data from Kinect.
        /// </summary>
        private SpeechRecognitionEngine speechEngine;

        private static RecognizerInfo GetKinectRecognizer()
        {
            foreach (RecognizerInfo recognizer in SpeechRecognitionEngine.InstalledRecognizers())
            {
                string value;
                recognizer.AdditionalInfo.TryGetValue("Kinect", out value);
                if ("True".Equals(value, StringComparison.OrdinalIgnoreCase) && "en-US".Equals(recognizer.Culture.Name, StringComparison.OrdinalIgnoreCase))
                {
                    return recognizer;
                }
            }

            return null;
        }

        public KinectInterface()
        {
            called = false;
            // Look through all sensors and start the first connected one.
            // This requires that a Kinect is connected at the time of app startup.
            // To make your app robust against plug/unplug, 
            // it is recommended to use KinectSensorChooser provided in Microsoft.Kinect.Toolkit (See components in Toolkit Browser).
            foreach (var potentialSensor in KinectSensor.KinectSensors)
            {
                if (potentialSensor.Status == KinectStatus.Connected)
                {
                    this.sensor = potentialSensor;
                    break;
                }
            }

            if (null != this.sensor)
            {
                try
                {
                    // Start the sensor!
                    this.sensor.Start();
                }
                catch (IOException)
                {
                    // Some other application is streaming from the same Kinect sensor
                    this.sensor = null;
                }
            }
            
            RecognizerInfo ri = GetKinectRecognizer();

            if (null != ri)
            {
                this.speechEngine = new SpeechRecognitionEngine(ri.Id);

                var choices = new Choices();
                choices.Add(new SemanticResultValue("turn lamp on", "LAMP ON"));
                choices.Add(new SemanticResultValue("turn the lamp on", "LAMP ON"));
                choices.Add(new SemanticResultValue("turn light on", "LAMP ON"));
                choices.Add(new SemanticResultValue("turn the light on", "LAMP ON"));
                choices.Add(new SemanticResultValue("turn the Table Lamp on", "LAMP ON"));
                choices.Add(new SemanticResultValue("turn Table Lamp on", "LAMP ON"));
                choices.Add(new SemanticResultValue("turn lamp off", "LAMP OFF"));
                choices.Add(new SemanticResultValue("turn the lamp of", "LAMP OFF"));
                choices.Add(new SemanticResultValue("turn light off", "LAMP OFF"));
                choices.Add(new SemanticResultValue("turn the light off", "LAMP OFF"));
                choices.Add(new SemanticResultValue("turn the Table Lamp off", "LAMP OFF"));
                choices.Add(new SemanticResultValue("turn Table Lamp off", "LAMP OFF"));
                choices.Add(new SemanticResultValue("turn printer on", "PRINTER ON"));
                choices.Add(new SemanticResultValue("turn the printer on", "PRINTER ON"));
                choices.Add(new SemanticResultValue("turn 3D printer on", "PRINTER ON"));
                choices.Add(new SemanticResultValue("turn the 3D printer on", "PRINTER ON"));
                choices.Add(new SemanticResultValue("turn printer off", "PRINTER OFF"));
                choices.Add(new SemanticResultValue("turn the printer off", "PRINTER OFF"));
                choices.Add(new SemanticResultValue("turn 3D printer off", "PRINTER OFF"));
                choices.Add(new SemanticResultValue("turn the 3D printer off", "PRINTER OFF"));
                choices.Add(new SemanticResultValue("computer", "COMPUTER"));
                choices.Add(new SemanticResultValue("house", "COMPUTER"));
                choices.Add(new SemanticResultValue("home", "COMPUTER"));

                var gb = new GrammarBuilder { Culture = ri.Culture };
                gb.Append(choices);

                var g = new Grammar(gb);

                speechEngine.LoadGrammar(g);

                /*// Create a grammar from grammar definition XML file.
                using (var memoryStream = new MemoryStream(Encoding.ASCII.GetBytes(Properties.Resources.SpeechGrammar)))
                {
                    var g = new Grammar(memoryStream);
                    speechEngine.LoadGrammar(g);
                }*/

                speechEngine.SpeechRecognized += SpeechRecognized;

                // For long recognition sessions (a few hours or more), it may be beneficial to turn off adaptation of the acoustic model. 
                // This will prevent recognition accuracy from degrading over time.
                speechEngine.UpdateRecognizerSetting("AdaptationOn", 0);

                speechEngine.SetInputToAudioStream(
                    sensor.AudioSource.Start(), new SpeechAudioFormatInfo(EncodingFormat.Pcm, 16000, 16, 1, 32000, 2, null));
                speechEngine.RecognizeAsync(RecognizeMode.Multiple);
            }
        }

        private void SpeechRecognized(object sender, SpeechRecognizedEventArgs e)
        {
            // Speech utterance confidence below which we treat speech as if it hadn't been heard
            const double ConfidenceThreshold = 0.3;

            if (e.Result.Confidence >= ConfidenceThreshold)
            {
                switch (e.Result.Semantics.Value.ToString())
                {
                    case "LAMP ON":
                        if (called)
                        {
                            WebRequest request = WebRequest.Create("http://192.168.1.147/toggleSwitch?sensor=Table%20Lamp&state=True");
                            WebResponse response = request.GetResponse();
                            called = false;
                        }
                        break;

                    case "LAMP OFF":
                        if (called)
                        {
                            WebRequest request = WebRequest.Create("http://192.168.1.147/toggleSwitch?sensor=Table%20Lamp&state=False");
                            WebResponse response = request.GetResponse();
                            called = false;
                        }
                        break;

                    case "PRINTER ON":
                        if (called)
                        {
                            WebRequest request = WebRequest.Create("http://192.168.1.147/toggleSwitch?sensor=3D%20Printer&state=True");
                            WebResponse response = request.GetResponse();
                            called = false;
                        }
                        break;

                    case "PRINTER OFF":
                        if (called)
                        {
                            WebRequest request = WebRequest.Create("http://192.168.1.147/toggleSwitch?sensor=3D%20Printer&state=False");
                            WebResponse response = request.GetResponse();
                            called = false;
                            called = false;
                        }
                        break;
                    case "COMPUTER":
                        called = true;
                        break;
                }
            }
        }

        public bool called;
    }
}
