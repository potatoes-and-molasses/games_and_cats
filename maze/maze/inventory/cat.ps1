$programs=@()
$credentials=@()
$items=@()
$level=1

$stats = @('programs','credentials','items','level')
function info([string]$type){
if ($stats -contains $type.tolower()){
$type+":`n" + (iex ('$' + $type))

}
else{
$stats | %{info $_}
}
}