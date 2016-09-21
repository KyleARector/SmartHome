using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Linq;
using System.ServiceProcess;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Kinect;
using Microsoft.Speech.AudioFormat;
using Microsoft.Speech.Recognition;
using System.IO;
using System.Net;
using System.Threading;

namespace KinectService
{
    public partial class KinectVoiceService : ServiceBase
    {
        public KinectVoiceService()
        {
            InitializeComponent();
        }

        protected override void OnStart(string[] args)
        {
            _thread = new Thread(_kinect.KinectStart);
            _thread.Start();
        }

        protected override void OnStop()
        {
            _kinect.KinectStop();
        }

        private KinectInterface _kinect = new KinectInterface();
        private Thread _thread;
    }

    class KinectInterface
    {
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

        /// <summary>
        /// Active Kinect sensor.
        /// </summary>
        private KinectSensor sensor;

        /// <summary>
        /// Speech recognition engine using audio data from Kinect.
        /// </summary>
        private SpeechRecognitionEngine speechEngine;

        /// <summary>
        /// Gets the metadata for the speech recognizer (acoustic model) most suitable to
        /// process audio from Kinect device.
        /// </summary>
        /// <returns>
        /// RecognizerInfo if found, <code>null</code> otherwise.
        /// </returns>
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

        /// <summary>
        /// Kinect start tasks
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        public void KinectStart()
        {
            called = false;

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
                    this.sensor.Start();
                }
                catch (IOException)
                {
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

                /*// Load grammar from XML file
                using (var memoryStream = new MemoryStream(Encoding.ASCII.GetBytes(Properties.Resources.SpeechGrammar)))
                {
                    var g = new Grammar(memoryStream);
                    speechEngine.LoadGrammar(g);
                }*/

                speechEngine.SpeechRecognized += SpeechRecognized;

                // For long recognition sessions (a few hours or more), it may be beneficial to turn off adaptation of the acoustic model. 
                // This will prevent recognition accuracy from degrading over time.
                ////speechEngine.UpdateRecognizerSetting("AdaptationOn", 0);

                speechEngine.SetInputToAudioStream(
                    sensor.AudioSource.Start(), new SpeechAudioFormatInfo(EncodingFormat.Pcm, 16000, 16, 1, 32000, 2, null));
                speechEngine.RecognizeAsync(RecognizeMode.Multiple);
            }
        }

        /// <summary>
        /// Execute Kinect stop tasks
        /// </summary>
        /// <param name="sender">object sending the event.</param>
        /// <param name="e">event arguments.</param>
        public void KinectStop()
        {
            if (null != this.sensor)
            {
                this.sensor.AudioSource.Stop();

                this.sensor.Stop();
                this.sensor = null;
            }

            if (null != this.speechEngine)
            {
                this.speechEngine.SpeechRecognized -= SpeechRecognized;
                this.speechEngine.RecognizeAsyncStop();
            }
        }

        public bool called { get; set; }
    }
}
