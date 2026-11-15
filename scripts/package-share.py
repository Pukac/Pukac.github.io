"""Package the client-facing website only, without project notes or backups."""
import hashlib
import json
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = ['index.html', 'output/pdf/jan-janda-profile-sk.pdf', 'output/pdf/jan-janda-profile-en.pdf']
out = root / 'output' / 'share'
out.mkdir(parents=True, exist_ok=True)
target = out / 'jan-janda-portfolio-v1.0.zip'
manifest = {'version': '1.0', 'files': []}
with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    for name in files:
        data = (root / name).read_bytes()
        archive.writestr(name, data)
        manifest['files'].append({'path': name, 'sha256': hashlib.sha256(data).hexdigest()})
    archive.writestr('START-HERE.txt',
        'Ján Janda | Software, AI & web solutions\n\n'
        'EN: Extract this archive and open index.html in your browser. Use EN in the top navigation for English. '
        'The two one-page professional profiles are in output/pdf. Contact Ján through the LinkedIn links in the portfolio.\n\n'
        'SK: Rozbaľte archív a otvorte index.html v prehliadači. Jazyk môžete prepnúť v hornej navigácii. '
        'Jednostranové profesijné profily nájdete v output/pdf. Kontakt je dostupný cez odkazy na LinkedIn.\n')
    archive.writestr('MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2))
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    for item in manifest['files']:
        assert hashlib.sha256(archive.read(item['path'])).hexdigest() == item['sha256']
print(target)
