from obb_anns import OBBAnns
from obb_anns.util import anns_from_text_anns

if __name__ == '__main__':
    anns = OBBAnns('deepscores_test.json')
    anns.load_annotations()
    anns.clear(clear_dataset_info=False)
    anns.dataset_info['description'] = "IMSLP test set"
    anns.dataset_info['year'] = 2022
    anns.dataset_info['contributor'] += ", Raphael Emberger"
    anns.dataset_info['date_created'] = "2022-01-28"
    anns.add_new_img_ann_pair(*anns_from_text_anns(anns, 'IMSLP651009_6_corr.png.anns', 'IMSLP651009_6_corr.png'))
    anns.add_new_img_ann_pair(*anns_from_text_anns(anns, 'IMSLP255036_16_corr.png.anns'))
    for img, ann_df in anns:
        print(anns.add_img_ann_pair(img, ann_df))
        print(img['filename'], ann_df.shape[0])

    anns.save_annotations('imslp_test.json')
