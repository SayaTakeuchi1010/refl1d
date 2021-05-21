import io
import requests
import h5py
import json

def load_url(file_url):
    print (file_url)
    fb = requests.get(file_url)
    f = h5py.File(io.BytesIO(fb.content))
    return f

def load_start_time(f, entry='unpolarized'):
    starttime = f['/' + entry + '/start_time'][()]
    return starttime

# Read JSON header to extract file and entry name (here entry name is '0' for illustration purposes)
source = 'https://ncnr.nist.gov/pub/'
# finelame : binary file name
filename = 'LionSi_kinetics4805.nxs.cdr'
# filename2 : .refl file name
filename2 = 'C:/Users/saya6/Documents/NCNR/kineticsDataAnalizer/LionSi_kinetics4805_0.refl'
print('filename2',filename2)
line = open(filename2, 'r').readline()
jsonstring = line.split('template_data')[1][2:-1]
d = json.loads(jsonstring)
print('d', d)
fileentrylist = []
for m in d['template']['modules']:
    if 'config' in m.keys():
        if 'intent' in m['config'].keys():
            if m['config']['intent'] == 'specular':
                for f in m['config']['filelist']:
                    fn = source + f['path']
                    entry = f['entries'][0]
                    fileentrylist.append([fn, entry])

print('fileentrylist', fileentrylist)

for (fn, entry) in fileentrylist:
    furl = load_url(fn)
    print('load_start_time(furl, entry=entry)', load_start_time(furl, entry=entry))
