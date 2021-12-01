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
    $sum = $depths[$a] + $depths[$b] + $depths[$c];

    if ($null -ne $prev) {
        $cnt += ($sum -gt $prev ? 1 : 0);
    }

    $prev = $sum
}

Write-Host "Sliding window increases $cnt times";
