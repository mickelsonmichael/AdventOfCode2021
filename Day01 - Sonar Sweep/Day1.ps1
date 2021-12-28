# https://adventofcode.com/2021/day/1

# ====================
# Part 1
# ====================

$depths = Get-Content .\Day1Input.json `
    | ConvertFrom-Json `
    | Select-Object -ExpandProperty "depths"

$a=0;
$b=1;
$cnt=0;

for (; $a -lt $depths.Length; $a++ && $b++ )
{
    $cnt += ($depths[$a] -lt $depths[$b] ? 1 : 0);
}

Write-Host "Depth increases $cnt times"

# ====================
# Part 2
# ====================

$a=0;
$b=1;
$c=2;
$cnt=0;
$prev=$null;

for (; $b -lt $depths.Length; $a++ && $b++ && $c++)
{
    # graham pointed out that that this summation is redunant
    # because we're given overlapping segments, we only need to compare the different depths, not those in common
    # say, for example, depths {A,B,C,D}. The first set would be [A,B,C] and the second set [B,C,D] leading to an equality check like:
    # A + B + C < B + C + D
    # subtracting both sides to simplify the equation leads us to a much simpler comparison that can be performed without a summation
    # A < D 
    # I will leave my original answer for posterity, but note there is a superior method
    $sum = $depths[$a] + $depths[$b] + $depths[$c];

    if ($null -ne $prev) {
        $cnt += ($sum -gt $prev ? 1 : 0);
    }

    $prev = $sum
}

Write-Host "Sliding window increases $cnt times";
