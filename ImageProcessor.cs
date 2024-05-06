using System.Drawing;
using System.Runtime.CompilerServices;
using Emgu.CV;
using Emgu.CV.CvEnum;
using Emgu.CV.PpfMatch3d;
using Emgu.CV.Reg;
using Emgu.CV.Structure;

namespace Pancake_Rotation_Tracker;

public class ImageProcessor{
    int beta = -50;
    float alpha = 1.2f;
    int n = 0;
    int radius = 50;
    string TemplatePath = "./ImageTemplates/BallBearing2.png";
    ImreadModes ImageReadType = ImreadModes.Unchanged;

    public void CheckImage(string FrameName, string VideoName, float sens){
        MCvScalar red = new MCvScalar(255,0,0);
        Mat template = CvInvoke.Imread(TemplatePath, ImageReadType);
        Mat frame = CvInvoke.Imread("./FrameExport/"+VideoName+"/"+FrameName, ImageReadType);
        List<Single> ResData = new List<Single>();
        List<Point> loc = new List<Point>();
        Mat[] res = new Mat[6];
        int h = template.Height/2;
        int w = template.Width/2;
        TemplateMatchingType[] MatchAlgorithms = [TemplateMatchingType.Ccoeff,
        TemplateMatchingType.CcoeffNormed,
        TemplateMatchingType.Sqdiff,
        TemplateMatchingType.SqdiffNormed,
        TemplateMatchingType.Ccorr,
        TemplateMatchingType.CcorrNormed];
        CvInvoke.CvtColor(frame,frame,ColorConversion.Bgr2Gray);
        CvInvoke.CvtColor(template, template,ColorConversion.Bgr2Gray);
        CvInvoke.ConvertScaleAbs(frame,frame,alpha,beta);
        for (int i = 0; i < MatchAlgorithms.Count(); i++){
            Mat TempMat = new Mat();
            CvInvoke.MatchTemplate(frame,template,TempMat,MatchAlgorithms[i]);
            TempMat.Save("./TestOutputs/"+MatchAlgorithms[i].ToString()+".jpg");
            res[i] = TempMat;
        }
        int Testing = 3;
        Single[,] PixelData = new Single[res[Testing].Height,res[Testing].Width];
        foreach (Single item in res[Testing].GetData()){
            ResData.Add(item);
        }
        int ResDataCount = ResData.Count();
        int W_0 = res[Testing].Width;
        for (int i = 0; i < ResDataCount; i++){
            if (ResData[i] <= sens){
                Point pos = new Point((i%W_0)+w,(i/W_0)+h);
                loc.Add(pos);
                CvInvoke.DrawMarker(frame,pos,red,MarkerTypes.Square,50);
            }
        }
        Console.WriteLine(loc.Count());
        frame.Save("output.jpg");
    }

}