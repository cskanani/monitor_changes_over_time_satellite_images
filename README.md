# monitor_changes_over_time_satellite_images
An end-to-end system using segmentation methods to detect infrastructural changes over a period of time.

# Steps to re-produce results
1. Download **Massachusetts Roads Dataset** from https://www.cs.toronto.edu/~vmnih/data/
    1. Convert images to .jpg
    1. Place images into ../road_data/train, ../road_data/test & ../road_data/val folders
1. Run train_road.py
    1. Trained model will be stored in saved_models directory
1. Download **Massachusetts Building Dataset** from https://www.cs.toronto.edu/~vmnih/data/
    1. Convert images to .jpg
    1. Place images into ../road_data/train, ../road_data/test & ../road_data/val folders
    1. Convert mask images from black-red to black-white using utils/red_to_white_mask.py
1. Run train_building.py
    1. Trained model will be stored in saved_models directory
1. You can test the accuracy of road and building detection using test_road.py and test_building.py files.
1. To get the infrastructural change over a period use the single_file_prediction.py file.

## Sample
| ![Pre Image](https://raw.githubusercontent.com/cskanani/measuring_impact_of_natural_calamities/master/demo_files/demo_images/infra_growth/original/1.jpg)  | ![Post Image](https://raw.githubusercontent.com/cskanani/measuring_impact_of_natural_calamities/master/demo_files/demo_images/infra_growth/original/4.jpg) | ![Detected Changes](https://raw.githubusercontent.com/cskanani/measuring_impact_of_natural_calamities/master/demo_files/demo_images/infra_growth/predictions/1_4.jpg) |
|:---:|:---:|:---:|
| Pre Image | Post Image | Detected Changes |

The Green part in "Detected Changes" image shows newly constructed roads and buildings, Red part shows destroyed roads and buildings.
