ls .\Renders\frames\ |
% { $_.Name.Split(".")[0..1] -join "." } |
group |
% {
  $start_number = (ls ".\Renders\frames\$($_.Name).*")[0].Name.Split(".")[2]
  ffmpeg -hide_banner -n -start_number $start_number -i ".\Renders\frames\$($_.Name).%04d.png" -pix_fmt yuv420p ".\Renders\clips\$($_.Name).mp4"
}