val1 = 42;
val2 = 0;
val3 = "hello";
val4 = [1, 2, 3];

echo("bool(42):", bool(val1));
echo("bool(0):", bool(val2));
echo("bool('hello'):", bool(val3));
echo("bool([1,2,3]):", bool(val4));

echo("int(3.7):", int(3.7));
echo("int(-2.2):", int(-2.2));

echo("str(3.14):", str(3.14));

list = [1, 2, 3];
echo("each([1,2,3]):", each(list));

cube(1);
