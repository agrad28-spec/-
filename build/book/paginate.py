import subprocess, re, json
pdf='/home/user/-/kitab_al_ulum_4_ibtidai.pdf'
n=int(re.search(r'Pages:\s+(\d+)',subprocess.check_output(['pdfinfo',pdf]).decode()).group(1))
pages={}
for i in range(1,n+1):
    t=subprocess.check_output(['pdftotext','-f',str(i),'-l',str(i),pdf,'-']).decode()
    for m in re.findall(r'ZZ([A-Z0-9]+)ZZ',t):
        pages.setdefault(m,i)
json.dump(pages,open('pages.json','w'))
print(pages)
