use <sample_lib.scad>;

function peg_r(n) = 1 + n * 0.25;
function peg_h(n) = 4 + n;

module peg_at(x, y, n=1) {
  translate([x, y, 2]) peg(r=peg_r(n), h=peg_h(n));
}

union() {
  base_plate(size=[20 + 4, 20, 2]);
  peg_at(5, 5, 2);
  peg_at(15, 5, 3);
  peg_at(10, 15, 4);
}
