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
    }
}
