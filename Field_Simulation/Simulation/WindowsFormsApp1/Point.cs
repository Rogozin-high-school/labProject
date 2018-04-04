using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WindowsFormsApp1
{
    class Point
    {
        public int[] coordinates;
        public Point(int[] arr)
        {
            this.coordinates = new int[2];
            this.coordinates[0] = arr[0];
            this.coordinates[1] = arr[1];
        }
        public static Point operator +(Point first,Point second)
        {
            int[] arr = { first.coordinates[0] + second.coordinates[0], first.coordinates[1] + second.coordinates[1] };
            return new Point(arr);
        }
        public float Distance(Point other)
        {
            float x2 = (float)Math.Pow(this.coordinates[0] - other.coordinates[0], 2.0);
            float y2 = (float)Math.Pow(this.coordinates[1] - other.coordinates[1], 2.0);
            return (float)Math.Sqrt(x2 + y2);
        }
        public float LenFromStart()
        {
            return (float)Math.Sqrt(Math.Pow(this.coordinates[0], 2.0) + Math.Pow(this.coordinates[1], 2.0));
        }
    }
}
