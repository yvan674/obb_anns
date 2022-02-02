from obb_anns import OBBAnns
from obb_anns.util import anns_from_text_anns

if __name__ == '__main__':
    anns = OBBAnns('in/deepscores_test.json')
    anns.load_annotations()
    anns.clear(clear_dataset_info=False)
    anns.dataset_info['description'] = "IMSLP test set"
    anns.dataset_info['year'] = 2022
    anns.dataset_info['contributor'] += ", Raphael Emberger"
    anns.dataset_info['date_created'] = "2022-01-28"
    fn = lambda l: [int(v * 0.769) for v in l]
    anns.add_new_img_ann_pair(*anns_from_text_anns(anns, 'in/IMSLP651009_6_corr.png.anns', 'in/IMSLP651009_6_corr.png'))
    anns.add_new_img_ann_pair(
        *anns_from_text_anns(anns, 'in/IMSLP255036_16_corr.png.anns', 'in/IMSLP255036_16_corr.png'))
    for i, (img, ann_df) in enumerate(anns):
        anns.visualize(img_idx=i, out_dir='out', annotation_set='deepscores', show=False)
        print(img['filename'], ann_df.shape[0])

    anns.save_annotations('in/imslp_test.json')
