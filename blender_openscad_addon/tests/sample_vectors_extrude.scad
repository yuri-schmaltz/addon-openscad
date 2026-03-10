// Test vector operations and list manipulation

a = [1, 2, 3];
b = [4, 5, 6];

echo("a:", a);
echo("b:", b);
echo("concat(a, b):", concat(a, b));
echo("norm(a):", norm(a));
echo("cross(a, b):", cross(a, b));

unsorted = [5, 2, 8, 1, 9, 3];
echo("unsorted:", unsorted);
echo("sort:", sort(unsorted));
echo("reverse:", reverse(unsorted));

// linear_extrude test
linear_extrude(height=10) {
  square([20, 20]);
}

// rotate_extrude test
rotate_extrude(angle=360) {
  circle(r=5);
}

// polygon test
polygon(points=[[0,0],[10,0],[5,10]]);
