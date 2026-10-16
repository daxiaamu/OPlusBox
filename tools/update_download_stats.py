"""Record GitHub APK download counters without losing previously observed assets."""
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote


def merge_assets(previous, releases):
    assets={str(item["id"]): dict(item, available=False) for item in previous}
    for release in releases:
        if release.get("draft"):
            continue
        for asset in release["assets"]:
            if not asset["name"].lower().endswith(".apk") or asset.get("state") != "uploaded":
                continue
            key=str(asset["id"])
            assets[key]={"id":asset["id"], "tag":release["tag_name"], "name":asset["name"],
                "downloads":max(assets.get(key,{}).get("downloads",0),asset["download_count"]),
                "publishedAt":release["published_at"], "available":True}
    return sorted(assets.values(),key=lambda item:(item["publishedAt"],item["id"]),reverse=True)


def render(repository, data):
    total=data["totalDownloads"]
    def escape(text):
        return text.replace("\\","\\\\").replace("|","\\|").replace("[","\\[").replace("]","\\]").replace("<","&lt;").replace("\n"," ").replace("\r"," ")
    lines=["# APK 下载统计", "", f"累计记录：**{total:,} 次**", "",
        f"最近统计变化：{data['updatedAt']}（UTC）", "",
        "| 版本 | APK | 下载次数 | 状态 |", "| --- | --- | ---: | --- |"]
    for asset in data["assets"]:
        tag=escape(asset["tag"])
        label=f"[{tag}](https://github.com/{repository}/releases/tag/{quote(asset['tag'],safe='')})" if asset["available"] else tag
        state="可下载" if asset["available"] else "已移除（保留最后记录）"
        lines.append(f"| {label} | {escape(asset['name'])} | {asset['downloads']:,} | {state} |")
    lines += ["", "每小时及发布事件后自动统计，也可在 Actions 中手动运行。", "",
        "数据来自 GitHub Release 资源的 download_count，表示下载次数，不是独立用户数；CDN 缓存命中不会计入 GitHub 下载量。统计启用前已删除的资源无法追溯。", ""]
    width=52+max(42,len(f"{total:,}")*7+16)
    right=width-52
    badge=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" role="img" aria-label="APK downloads: {total}"><rect width="52" height="20" fill="#555"/><rect x="52" width="{right}" height="20" fill="#1675bd"/><g fill="white" text-anchor="middle" font-family="Arial,sans-serif" font-size="11"><text x="26" y="14">APK</text><text x="{52+right/2}" y="14">{total:,}</text></g></svg>\n'
    return "\n".join(lines),badge


def main():
    repository=os.environ["GITHUB_REPOSITORY"]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",repository):
        raise ValueError("Invalid repository")
    response=subprocess.check_output(["gh","api","--paginate","--slurp",f"repos/{repository}/releases?per_page=100"],text=True,encoding="utf-8")
    releases=[release for page in json.loads(response) for release in page]
    output=Path("stats"); output.mkdir(exist_ok=True)
    target=output/"downloads.json"
    previous=json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
    if previous and previous["repository"]!=repository:
        raise ValueError("Snapshot belongs to another repository")
    assets=merge_assets(previous.get("assets",[]),releases)
    data={"schemaVersion":1,"repository":repository,
        "updatedAt":previous.get("updatedAt") if previous.get("assets")==assets else datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "totalDownloads":sum(asset["downloads"] for asset in assets),"assets":assets}
    if not data["updatedAt"]:
        data["updatedAt"]=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    markdown,badge=render(repository,data)
    target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (output/"downloads.md").write_text(markdown,encoding="utf-8")
    (output/"downloads.svg").write_text(badge,encoding="utf-8")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"],"a",encoding="utf-8") as stream:
            stream.write(markdown)
    print(f"APK downloads: {data['totalDownloads']}; recorded assets: {len(assets)}")


if __name__=="__main__":
    main()
