Add-Type -ReferencedAssemblies System.Drawing -TypeDefinition @"
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
public static class PaintCut {
  public static string Cut(string srcPath, string destPath) {
    using (Bitmap src = new Bitmap(srcPath)) {
      int left = (int)(src.Width * 0.18);
      int top = (int)(src.Height * 0.16);
      int right = (int)(src.Width * 0.72);
      int bottom = (int)(src.Height * 0.82);
      int cw = right - left, ch = bottom - top;
      Bitmap canvas = new Bitmap(cw, ch, PixelFormat.Format32bppArgb);
      using (Graphics g = Graphics.FromImage(canvas))
        g.DrawImage(src, new Rectangle(0,0,cw,ch), new Rectangle(left,top,cw,ch), GraphicsUnit.Pixel);
      BitmapData d = canvas.LockBits(new Rectangle(0,0,cw,ch), ImageLockMode.ReadOnly, PixelFormat.Format32bppArgb);
      int bytes = Math.Abs(d.Stride) * ch;
      byte[] px = new byte[bytes];
      Marshal.Copy(d.Scan0, px, 0, bytes);
      int stride = d.Stride;
      canvas.UnlockBits(d);
      int minX = cw, minY = ch, maxX = 0, maxY = 0;
      bool found = false;
      for (int y = 0; y < ch; y++) {
        int row = y * stride;
        for (int x = 0; x < cw; x++) {
          int i = row + x * 4;
          byte b = px[i], gr = px[i+1], r = px[i+2];
          int mn = Math.Min(r, Math.Min(gr, b));
          int mx = Math.Max(r, Math.Max(gr, b));
          if (!(mn >= 245 && (mx - mn) < 12)) {
            found = true;
            if (x < minX) minX = x;
            if (y < minY) minY = y;
            if (x > maxX) maxX = x;
            if (y > maxY) maxY = y;
          }
        }
      }
      if (!found) throw new Exception("empty");
      int pad = 20;
      minX = Math.Max(0, minX - pad); minY = Math.Max(0, minY - pad);
      maxX = Math.Min(cw-1, maxX + pad); maxY = Math.Min(ch-1, maxY + pad);
      int w = maxX - minX + 1, h = maxY - minY + 1;
      Bitmap outBmp = new Bitmap(w, h, PixelFormat.Format32bppArgb);
      using (Graphics g2 = Graphics.FromImage(outBmp))
        g2.DrawImage(canvas, new Rectangle(0,0,w,h), new Rectangle(minX,minY,w,h), GraphicsUnit.Pixel);
      canvas.Dispose();
      BitmapData d2 = outBmp.LockBits(new Rectangle(0,0,w,h), ImageLockMode.ReadWrite, PixelFormat.Format32bppArgb);
      int bytes2 = Math.Abs(d2.Stride) * h;
      byte[] px2 = new byte[bytes2];
      Marshal.Copy(d2.Scan0, px2, 0, bytes2);
      for (int i = 0; i < px2.Length; i += 4) {
        byte b = px2[i], gr = px2[i+1], r = px2[i+2];
        int mn = Math.Min(r, Math.Min(gr, b));
        int mx = Math.Max(r, Math.Max(gr, b));
        if (mn >= 242 && (mx - mn) < 14) px2[i+3] = 0;
        else if (mn >= 220 && (mx - mn) < 18) {
          int a = (int)(255.0 * (242 - mn) / 22.0);
          if (a < 0) a = 0; if (a > 255) a = 255;
          px2[i+3] = (byte)a;
        }
      }
      Marshal.Copy(px2, 0, d2.Scan0, bytes2);
      outBmp.UnlockBits(d2);
      outBmp.Save(destPath, ImageFormat.Png);
      string info = w + "x" + h;
      outBmp.Dispose();
      return info;
    }
  }
}
"@
