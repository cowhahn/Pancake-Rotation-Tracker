using System.Drawing;
using System.IO;
using System.Runtime.InteropServices;
using Emgu.CV.Bioinspired;

namespace Pancake_Rotation_Tracker;

public class DataProcessor{

    public static bool CheckForPoint(List<Point> points, Point CheckPoint){
        foreach (Point item in points){
            if (item == CheckPoint) return true;
        }
        return false;
    }
    public static int NegPosDist(int value){
        return (value*2)+1;
    }
    public static List<int> GetIndexes(List<Point> LastPoints, List<Point> points){
        List<int> indexes = new List<int>();
        foreach (Point item in points){
            bool FoundPoint = false;
            int DistCounter = 0;
            while (!FoundPoint){
                for(int yCounter = -DistCounter; yCounter <= DistCounter; yCounter++){
                    if(FoundPoint) break;
                    for (int xCounter = -DistCounter; xCounter <= DistCounter; xCounter++){
                        FoundPoint = CheckForPoint(LastPoints,new Point(item.X+xCounter,item.Y+yCounter));
                        if(FoundPoint){
                            indexes.Add(LastPoints.IndexOf(new Point(item.X+xCounter,item.Y+yCounter)));
                            break;
                        }
                    }
                }
                DistCounter++;
            }
        }
        return indexes;
    }
    public static List<Point> SortPoints(List<Point> LastPoints, List<Point> points){
        List<int> indexes = GetIndexes(LastPoints,points);
        Point[] SortedPoints = new Point[indexes.Count()];
        for (int i = 0; i < indexes.Count(); i++){
            SortedPoints[indexes[i]] = points[i];
        }
        return SortedPoints.ToList();
    }
    public static Point CenterOfMass(List<Point> points){
        Point COM = new Point();
        foreach (Point item in points){
            COM.X += item.X;
            COM.Y += item.Y;
        }
        COM.X /= points.Count();
        COM.Y /= points.Count();
        return COM;
    }
    public static Point RelativePos(Point COM, Point point){
        return new Point(point.X-COM.X,point.Y-COM.Y);
    }
    public static double AngularVelocity(Point RelativeFrame0, Point RelativeFrame1, int fps){
        double angle1 = Math.Atan2(RelativeFrame0.Y, RelativeFrame0.X);
        double angle2 = Math.Atan2(RelativeFrame1.Y, RelativeFrame1.X);
        double angle  = new double();
        if (angle1 < 0 && angle2 > 0){
            angle = (Math.PI - angle1) + angle2;
        }
        else if (angle1 > 0 && angle2 < 0){
            angle = -(Math.PI - angle2) - angle1;
        }
        else{
            angle = angle2 - angle1;
        }
        while (angle < -Math.PI){
            angle += Math.PI;
        }
        while (angle > Math.PI){
            angle -= Math.PI;
        }
        return angle*fps;
    }
    public static double AverageAngularVelocityOfCluster(List<Point> points0, List<Point> points1, int fps){
        Point COM0 = CenterOfMass(points0);
        Point COM1 = CenterOfMass(points1);
        double velocity = new double();
        for (int i =0; i < points1.Count(); i++){
            try{
                velocity += AngularVelocity(RelativePos(COM0,points0[i]), RelativePos(COM1,points1[i]), fps);
            }
            catch{
                velocity +=0;
            }
            
        }
        velocity /= points1.Count();
        return velocity;
    }

    public static double AverageVideoVelocity(List<double> velocities){
        double VideoVelocity = new double();
        foreach (double item in velocities){
            VideoVelocity += item;
        }
        VideoVelocity /= velocities.Count();
        return VideoVelocity;
    }
}