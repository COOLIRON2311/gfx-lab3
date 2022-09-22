using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace lab3
{
    public partial class Form1 : Form
    {

        Color col;
        Bitmap img;
        Bitmap tempImg;
        Graphics g;
        Pen pen;
        bool mouseDown;
        int x, y;
        public Form1()
        {
            col = Color.Black;
            InitializeComponent();
            pen = new Pen(col, 5);
            pen.StartCap = pen.EndCap = System.Drawing.Drawing2D.LineCap.Round;
            img = new Bitmap(Width, Height);
            g = Graphics.FromImage(img);
            g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
            mouseDown = false;
        }

        private void pictureBox1_MouseDown(object sender, MouseEventArgs e)
        {
            mouseDown = true;
            x = e.X;
            y = e.Y;
        }

        private void pictureBox1_MouseUp(object sender, MouseEventArgs e)
        {
            mouseDown = false;
        }

        private void pictureBox1_MouseClick(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Right)
            {
                LinearFloodFillWithImage(e.X, e.Y);
                // img.Save("image.png");
            }
        }

        private void Form1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Escape)
            {
                img = new Bitmap(Width, Height);
                g = Graphics.FromImage(img);
                pictureBox1.Image = img;
            }
        }

        private void pictureBox1_MouseMove(object sender, MouseEventArgs e)
        {
            if (mouseDown && e.Button == MouseButtons.Left)
            {
                g.DrawLine(pen, new Point(x, y), e.Location);
                x = e.X;
                y = e.Y;
                pictureBox1.Image = img;
            }
        }

        private void floodFill(int x, int y)
        {
            Color targetColor = img.GetPixel(x, y);
            if (targetColor == col)
                return;
            Stack<Point> stack = new Stack<Point>();
            stack.Push(new Point(x, y));
            while (stack.Count > 0)
            {
                Point p = stack.Pop();
                if (img.GetPixel(p.X, p.Y) == targetColor)
                {
                    img.SetPixel(p.X, p.Y, col);
                    if (p.X > 0)
                        stack.Push(new Point(p.X - 1, p.Y));
                    if (p.X < img.Width - 1)
                        stack.Push(new Point(p.X + 1, p.Y));
                    if (p.Y > 0)
                        stack.Push(new Point(p.X, p.Y - 1));
                    if (p.Y < img.Height - 1)
                        stack.Push(new Point(p.X, p.Y + 1));
                }
            }
            pictureBox1.Image = img;
        }

        private void LinearFloodFill(int x, int y)
        {
            Color targetColor = Color.FromArgb(0, 0, 0, 0);
            if (targetColor == col)
                return;
            Stack<Point> stack = new Stack<Point>();
            stack.Push(new Point(x, y));

            while (stack.Count > 0)
            {
                Point p = stack.Pop();

                if (img.GetPixel(p.X, p.Y) != targetColor)
                    continue;

                int leftBorder = p.X;
                int rightBorder = p.X;

                for (int i = p.X; i < img.Width; i++)
                {
                    if (img.GetPixel(i, p.Y) != targetColor)
                    {
                        break;
                    }

                    rightBorder = i;

                    img.SetPixel(i, p.Y, col);
                }

                for (int i = p.X - 1; i >= 0; i--)
                {
                    if (img.GetPixel(i, p.Y) != targetColor)
                    {
                        break;
                    }

                    leftBorder = i;

                    img.SetPixel(i, p.Y, col);
                }

                for (int i = leftBorder; i <= rightBorder; i++)
                {
                    if (p.Y + 1 < img.Height)
                        stack.Push(new Point(i, p.Y + 1));
                }

                for (int i = leftBorder; i <= rightBorder; i++)
                {
                    if (p.Y - 1 > 0)
                        stack.Push(new Point(i, p.Y - 1));
                }

            }
                pictureBox1.Image = img;
        }
        private void LinearFloodFillWithImage(int x, int y)
        {
            Color targetColor = Color.FromArgb(0, 0, 0, 0);
            /*if (targetColor == col)
                return;*/
            Stack<Point> stack = new Stack<Point>();
            stack.Push(new Point(x, y));

            while (stack.Count > 0)
            {
                Point p = stack.Pop();

                if (img.GetPixel(p.X, p.Y) != targetColor)
                    continue;

                int leftBorder = p.X;
                int rightBorder = p.X;

                for (int i = p.X; i < img.Width; i++)
                {
                    if (img.GetPixel(i, p.Y) != targetColor)
                    {
                        break;
                    }

                    rightBorder = i;

                    img.SetPixel(i, p.Y, tempImg.GetPixel(i%tempImg.Width,p.Y%tempImg.Height));
                }

                for (int i = p.X - 1; i >= 0; i--)
                {
                    if (img.GetPixel(i, p.Y) != targetColor)
                    {
                        break;
                    }

                    leftBorder = i;

                    img.SetPixel(i, p.Y, tempImg.GetPixel(i % tempImg.Width, p.Y % tempImg.Height));
                }

                for (int i = leftBorder; i <= rightBorder; i++)
                {
                    if (p.Y + 1 < img.Height)
                        stack.Push(new Point(i, p.Y + 1));
                }

                for (int i = leftBorder; i <= rightBorder; i++)
                {
                    if (p.Y - 1 > 0)
                        stack.Push(new Point(i, p.Y - 1));
                }

            }
            pictureBox1.Image = img;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            ColorDialog colorDialog = new ColorDialog();
            if (colorDialog.ShowDialog() == DialogResult.OK)
            {
                col = colorDialog.Color;
                pen = new Pen(col, 5);
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog dlg = new OpenFileDialog())
            {
                dlg.Title = "Open Image";
                dlg.Filter = "bmp files (*.bmp)|*.bmp";

                if (dlg.ShowDialog() == DialogResult.OK)
                {
                    tempImg = new Bitmap(dlg.FileName);
                }
            }
        }
    }
}
