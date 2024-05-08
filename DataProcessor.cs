using System.Drawing;
using System.IO;
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
}