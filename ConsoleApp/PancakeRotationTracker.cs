using System.Drawing;
using System.IO;
using Emgu.CV;

namespace Pancake_Rotation_Tracker;

public class PancakeRotationTracker{
        static double DoAvgCalculation(List<List<Point>> MarkedData, int fps){
            List<double> velocities = new List<double>();
            for (int i = 1; i < MarkedData.Count(); i++){
                velocities.Add(DataProcessor.AverageAngularVelocityOfCluster(MarkedData[i-1],MarkedData[i], fps));
            }
            return DataProcessor.AverageVideoVelocity(velocities);
        }
        static void Main(string[] args){
        float sens = .8f;
        int OriginCount = new int();
        List<List<Point>> MarkedData = new List<List<Point>>();
        string? InputPath = null;
        while (InputPath == null){
            Console.Write("Please enter videofile name: ");
            InputPath = Console.ReadLine();
        }
        int length = VideoFrameSplitter.ExtractImages(InputPath);
        Directory.CreateDirectory("./MarkedFrames/"+InputPath);
        for (int i = 0; i<length; i++){
            string FrameName = "frame"+i+".jpg";
            string VideoName = InputPath;
            List<Point> SortedLoc = new List<Point>();
            List<Point> loc = ImageProcessor.CheckImage(FrameName,VideoName, sens, new Mat());
            if (FrameName == "frame0.jpg") OriginCount = loc.Count();
            while (loc.Count() != OriginCount){
                if (loc.Count() > OriginCount){
                    sens -= .01f;
                }
                else{
                    sens += .01f;
                }
                loc = ImageProcessor.CheckImage(FrameName,VideoName, sens, new Mat());
                Console.WriteLine("Adjusting sens because incorrect number of balls");
            }
            Console.WriteLine("Processing frame: "+i);
            if (i==0) {
                SortedLoc = DataProcessor.SortPoints(loc,loc);
            }
            if (i != 0){
                SortedLoc = DataProcessor.SortPoints(MarkedData[i-1], loc);
            }
            MarkedData.Add(SortedLoc);
            Console.WriteLine(SortedLoc.Count());
        }
        Console.WriteLine("Amount of Frames: "+MarkedData.Count());
        Console.WriteLine("The average Angular Velocity is: "+ DoAvgCalculation(MarkedData,240));
    }
}