import unittest
from update_download_stats import merge_assets


def release(asset_id=1,count=3,name="box.apk",draft=False):
    return {"draft":draft,"tag_name":"v1","published_at":"2026-10-17T00:00:00Z",
        "assets":[{"id":asset_id,"name":name,"state":"uploaded","download_count":count}]}


class DownloadStatsTest(unittest.TestCase):
    def test_only_published_apks_count(self):
        assets=merge_assets([], [release(),release(2,name="notes.txt"),release(3,draft=True)])
        self.assertEqual([1],[a["id"] for a in assets])
    def test_existing_asset_never_double_counts_or_decreases(self):
        before=merge_assets([], [release(count=7)])
        after=merge_assets(before,[release(count=5)])
        self.assertEqual(7,sum(a["downloads"] for a in after))
        self.assertEqual(1,len(after))
    def test_deleted_asset_retains_last_counter(self):
        assets=merge_assets(merge_assets([], [release(count=7)]),[])
        self.assertEqual(7,assets[0]["downloads"])
        self.assertFalse(assets[0]["available"])
    def test_replaced_asset_keeps_both_observed_counters(self):
        assets=merge_assets(merge_assets([], [release(count=7)]),[release(2,count=4)])
        self.assertEqual(11,sum(a["downloads"] for a in assets))
        self.assertEqual(1,sum(a["available"] for a in assets))

if __name__=="__main__": unittest.main()
