
function link([string]$link,[string]$target){
#link C: C:\linktoc
C:\SysInternals\junction.exe $target $link
}

function room([string]$path,[array]$files,[string]$title,[string]$message){
mkdir $path
if($files){$files | %{copy $_ ($path +'\'+ ($_ -split '\\')[-1])}
}
if($message -and $title){
$message > ($path + '\' + $title)
}
}

$fnames = 'abcdefghijklmnopqrstuvwxyz0123456789'

$TAR = 'C:\maze\'
cd $TAR


room maze 'C:\maze\readme.tiexti'
room maze\inventory 'C:\maze\cat.ps1'
room maze\enterance 
room maze\enterance\bestroomevah -title 'note' -message 'many directories contain all sorts of useful files!'
room maze\enterance\reasonableroom -title 'nope' -message 'many directories contain whimsical blabberings of no sense or purpose'
room maze\enterance\tunnel -title 'choices' -message 'whoops'
link maze\enterance maze\enterance\tunnel\here 
room maze\enterance\tunnel\there
room maze\enterance\tunnel\everywhere
room 'maze\enterance\tunnel\everywhere\keep going'
room 'maze\enterance\tunnel\everywhere\keep going\almost there'
link maze\enterance\tunnel\everywhere\ 'maze\enterance\tunnel\everywhere\keep going\almost there\just a bit more'
room 'maze\enterance\tunnel\there\Program Fails'
room 'maze\enterance\tunnel\there\Program Fails (x86)' -title 'the first rule of tautology club' -message 'is the first rule of tautology club'
link 'maze\enterance\tunnel\there\Program Fails' 'maze\enterance\tunnel\there\Windows'
room 'maze\enterance\tunnel\there\Balconies' -title 'P@ssw0rd135t P@ssw0rd' -message '109470914 << 18 or something' #8349602515215087463
room 'maze\enterance\tunnel\there\Doors' 'C:\maze\espionage cabbage.pfx'
room 'maze\enterance\tunnel\there\Program Fails\guess what'

