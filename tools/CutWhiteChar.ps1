Add-Type -ReferencedAssemblies System.Drawing -TypeDefinition @"
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
public static class CutWhiteChar {
  static bool IsCanvas(byte r, byte g, byte b) {
    int mn = Math.Min(r, Math.Min(g, b));
    int mx = Math.Max(r, Math.Max(g, b));
    return mn >= 246 && (mx - mn) < 12;
  }
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
      BitmapData d = canvas.LockBits(new Rectangle(0,0,cw,ch), ImageLockMode.ReadWrite, PixelFormat.Format32bppArgb);
      int stride = d.Stride;
      int bytes = Math.Abs(stride) * ch;
      byte[] px = new byte[bytes];
      Marshal.Copy(d.Scan0, px, 0, bytes);
      bool[] ink = new bool[cw * ch];
      for (int y = 0; y < ch; y++) {
        for (int x = 0; x < cw; x++) {
          int i = y * stride + x * 4;
          ink[y * cw + x] = !IsCanvas(px[i+2], px[i+1], px[i]);
        }
      }
      bool[] dil = new bool[cw * ch];
      int rad = 2;
      for (int y = 0; y < ch; y++) {
        for (int x = 0; x < cw; x++) {
          bool hit = false;
          for (int dy = -rad; dy <= rad && !hit; dy++) {
            int yy = y + dy; if (yy < 0 || yy >= ch) continue;
            for (int dx = -rad; dx <= rad; dx++) {
              int xx = x + dx; if (xx < 0 || xx >= cw) continue;
              if (ink[yy * cw + xx]) { hit = true; break; }
            }
          }
          dil[y * cw + x] = hit;
        }
      }
      bool[] seen = new bool[cw * ch];
      Queue<int> q = new Queue<int>();
      Action<int,int> tryPush = (x, y) => {
        if (x < 0 || y < 0 || x >= cw || y >= ch) return;
        int id = y * cw + x;
        if (seen[id] || dil[id]) return;
        seen[id] = true;
        q.Enqueue(id);
      };
      for (int x = 0; x < cw; x++) { tryPush(x, 0); tryPush(x, ch-1); }
      for (int y = 0; y < ch; y++) { tryPush(0, y); tryPush(cw-1, y); }
      int[] dx4 = new int[] {1,-1,0,0};
      int[] dy4 = new int[] {0,0,1,-1};
      while (q.Count > 0) {
        int id = q.Dequeue();
        int x = id % cw, y = id / cw;
        for (int k = 0; k < 4; k++) tryPush(x + dx4[k], y + dy4[k]);
      }
      int minX = cw, minY = ch, maxX = 0, maxY = 0;
      bool found = false;
      for (int y = 0; y < ch; y++) {
        for (int x = 0; x < cw; x++) {
          int id = y * cw + x;
          int i = y * stride + x * 4;
          if (seen[id]) px[i+3] = 0;
          else {
            found = true;
            if (x < minX) minX = x;
            if (y < minY) minY = y;
            if (x > maxX) maxX = x;
            if (y > maxY) maxY = y;
          }
        }
      }
      Marshal.Copy(px, 0, d.Scan0, bytes);
      canvas.UnlockBits(d);
      if (!found) throw new Exception("empty");
      int pad = 16;
      minX = Math.Max(0, minX - pad); minY = Math.Max(0, minY - pad);
      maxX = Math.Min(cw-1, maxX + pad); maxY = Math.Min(ch-1, maxY + pad);
      int w = maxX - minX + 1, h = maxY - minY + 1;
      Bitmap outBmp = new Bitmap(w, h, PixelFormat.Format32bppArgb);
      using (Graphics g2 = Graphics.FromImage(outBmp))
        g2.DrawImage(canvas, new Rectangle(0,0,w,h), new Rectangle(minX,minY,w,h), GraphicsUnit.Pixel);
      canvas.Dispose();
      outBmp.Save(destPath, ImageFormat.Png);
      string info = w + "x" + h;
      outBmp.Dispose();
      return info;
    }
  }

  public static void FillInteriorWhite(string path) {
    Bitmap src = new Bitmap(path);
    Bitmap bmp = new Bitmap(src.Width, src.Height, PixelFormat.Format32bppArgb);
    using (Graphics g = Graphics.FromImage(bmp)) g.DrawImage(src, 0, 0, src.Width, src.Height);
    src.Dispose();
    int w = bmp.Width, h = bmp.Height;
    BitmapData d = bmp.LockBits(new Rectangle(0,0,w,h), ImageLockMode.ReadWrite, PixelFormat.Format32bppArgb);
    int stride = d.Stride;
    int bytes = Math.Abs(stride) * h;
    byte[] px = new byte[bytes];
    Marshal.Copy(d.Scan0, px, 0, bytes);
    bool[] empty = new bool[w * h];
    for (int y = 0; y < h; y++) {
      for (int x = 0; x < w; x++) {
        int i = y * stride + x * 4;
        empty[y * w + x] = px[i+3] < 40;
      }
    }
    bool[] edge = new bool[w * h];
    Queue<int> q = new Queue<int>();
    Action<int,int> push = (x, y) => {
      if (x < 0 || y < 0 || x >= w || y >= h) return;
      int id = y * w + x;
      if (edge[id] || !empty[id]) return;
      edge[id] = true;
      q.Enqueue(id);
    };
    for (int x = 0; x < w; x++) { push(x, 0); push(x, h-1); }
    for (int y = 0; y < h; y++) { push(0, y); push(w-1, y); }
    int[] dx = new int[] {1,-1,0,0};
    int[] dy = new int[] {0,0,1,-1};
    while (q.Count > 0) {
      int id = q.Dequeue();
      int x = id % w, y = id / w;
      for (int k = 0; k < 4; k++) push(x + dx[k], y + dy[k]);
    }
    for (int y = 0; y < h; y++) {
      for (int x = 0; x < w; x++) {
        int id = y * w + x;
        if (empty[id] && !edge[id]) {
          int i = y * stride + x * 4;
          px[i] = 255; px[i+1] = 255; px[i+2] = 255; px[i+3] = 255;
        }
      }
    }
    Marshal.Copy(px, 0, d.Scan0, bytes);
    bmp.UnlockBits(d);
    bmp.Save(path, ImageFormat.Png);
    bmp.Dispose();
  }
}
"@
