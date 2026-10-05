import hashlib,json,os,pathlib,re,subprocess,tempfile,urllib.request,urllib.parse

def download_verified(url,expected_sha,expected_size):
    if urllib.parse.urlparse(url).scheme!='https': raise ValueError('HTTPS required')
    class HttpsOnlyRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,req,fp,code,msg,headers,newurl):
            if urllib.parse.urlparse(newurl).scheme!='https': raise ValueError('Non-HTTPS redirect')
            return super().redirect_request(req,fp,code,msg,headers,newurl)
    opener=urllib.request.build_opener(HttpsOnlyRedirect())
    with opener.open(urllib.request.Request(url,headers={'User-Agent':'OPLUSBox-release-validator'}),timeout=30) as response:
        digest=hashlib.sha256(); total=0
        while True:
            block=response.read(1024*1024)
            if not block: break
            total+=len(block)
            if total>expected_size: raise ValueError('Oversize CDN response')
            digest.update(block)
        return total==expected_size and digest.hexdigest()==expected_sha

def main():
    event=json.loads(pathlib.Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    release=event['release']; channel='beta' if release['prerelease'] else 'stable'
    assets=[a for a in release['assets'] if a['name'].endswith('.apk')]
    assert len(assets)==1
    apk=pathlib.Path('release.apk')
    aapt=sorted(pathlib.Path(os.environ['ANDROID_HOME'],'build-tools').glob('*/aapt2'))[-1]
    badging=subprocess.check_output([str(aapt),'dump','badging',str(apk)],text=True)
    identity=re.search(r"^package: name='([^']+)' versionCode='(\d+)' versionName='([^']+)'",badging,re.M)
    assert identity and identity[1]=='com.daxiaamu.oplusbox'
    code=int(identity[2]); name=identity[3]; assert release['tag_name'].removeprefix('v')==name
    assert ('beta' in name.lower())==(channel=='beta'), 'APK versionName must match release channel'
    sha=hashlib.sha256(apk.read_bytes()).hexdigest(); size=apk.stat().st_size
    policy=json.loads(pathlib.Path(f'update/policy-{channel}.json').read_text(encoding='utf-8-sig'))
    forced=policy['maxForcedVersionCode']; revision=policy['policyRevision']
    assert type(forced)==int and type(revision)==int and 0<=forced<code and revision>0 and policy['reason']
    target=pathlib.Path('update/update-beta.json' if channel=='beta' else 'update/update.json')
    if target.exists():
        previous=json.loads(target.read_text()); assert revision>previous['policyRevision'] and code>previous['versionCode']
    official=assets[0]['browser_download_url']; assert urllib.parse.urlparse(official).hostname=='github.com'
    candidates=[f'https://{host}/{official}' for host in ['ghfast.top','gh-proxy.com','ghproxy.net','gh.llkk.cc','ghp.keleyaa.com','gh.monlor.com','ghproxy.vip','gh.jasonzeng.dev','gh.3w.pm','gh-proxy.org']]
    good=[]
    for url in candidates:
        try:
            if download_verified(url,sha,size): good.append(url)
        except Exception as error: print(f'CDN unavailable: {urllib.parse.urlparse(url).hostname}: {type(error).__name__}')
        if len(good)>=5: break
    assert len({urllib.parse.urlparse(u).hostname for u in good})>=5, 'Five verified CDN hosts required; previous manifest preserved'
    good.append(official)
    data=dict(schemaVersion=1,channel=channel,versionCode=code,versionName=name,publishedAt=release['published_at'],changelog=release.get('body') or '',maxForcedVersionCode=forced,policyRevision=revision,url=good[0],urls=good,sha256=sha,size=size,releaseUrl=release['html_url'],policyReason=policy['reason'])
    temporary=target.with_suffix('.tmp');temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temporary.replace(target)
if __name__=='__main__':main()
