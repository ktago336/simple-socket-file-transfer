# Simple file transfer
File transfering using sockets<br>
Run with parameters: sync.py "ip" "mode"<br>
<h3>ip</h3>If recieving files use your local ip to bind. If sending use destination ip. Defalt port: 5555<br>
<h3>mode</h3> Use "s" parameter to set the send mode or "r" for recieve mode<hr>
<h2>setupsync.py</h2> Module functions 
<h4>firstRun()</h4>sets up folder "files" and "data.cfg" in current directory. "files" - synchronized files, "data.cfg" - stores "files" folder full filepaths as keys of dict and md5 hash as value for changes check
<h4>createCfg(path)</h4>in current 'path' ("files" folder) walks all directories and saves full file paths in "data.cfg"
<h4>checkSum(path)</h4>compares check sums from "data.cfg" and in 'path', in case of difference of check sums updates this file, and in case if file is not included in "data.cfg" updates it
<h4>updateData(path)</h4>choose recieve mode for example on server and send mode on your PC
