
md alice-pvk
cd alice-pvk

openssl rsa -in ..\alice-key.pem -outform PVK -pvk-strong -out alice-cert-pvk.pvk

cp ../alice-cert.der alice-cert-pvk.cer

pvk2pfx.exe /pvk alice-cert-pvk.pvk /pi password /spc alice-cert-pvk.cer /pfx alice-cert-pvk.pfx /po password

cp alice-cert-pvk.pfx ../alice-cert-pvk.p12

rem fails
certutil -v -p password,password -MergePFX alice-cert-pvk.cer,alice-cert-pvk.pvk alice-cert-pvk.pfx
