---
layout: post
title:  "Properties and differences of clouds and cloud clusters"
date:   2024-04-03 15:30:00 +0200
categories: jekyll update
---

# Properties and differences of clouds and cloud clusters[^1].

On the subpage [cloud and cluster identification](https://sdm-eurec4a.readthedocs.io/en/documentation/source/cloud_and_cluster_identification.html) from the documentation of the [sdm-eurec4a](https://github.com/nilsnevertree/sdm-eurec4a) repository, it is explained how clouds and cloud clusters were identified.
On this post, we will show the typical extent of the identified clouds and some other properties.

For the cloud clusters, the ``min_duration_cloud_holes`` was set to 5 seconds. 
This means that the cloud clusters are identified by the connected clouds with a hole of less than 5 seconds.

### An example as in [cloud and cluster identification](https://sdm-eurec4a.readthedocs.io/en/documentation/source/cloud_and_cluster_identification.html)

Because the ATR often flew through clouds with less droplets, the cloud_mask and rain_mask have “holes” along the time dimension. Here is an example image which shows an example cloud clusters in the ATR dataset. Each one of the spikes will be identified as an individual cloud by the script shown above. The script below ignores holes between the clouds if they do not exceed a specified duration.

<!-- ![Image]({{"assets/images/compare_cluster_and_clouds/example_cloud_cluster_identification.png", | relative_url }}) -->
<img src="{{"assets/images/compare_cluster_and_clouds/example_cloud_cluster_identification.png", | relative_url }}" alt="example_cloud_cluster_identification" width="66%"/>

### Using the ``rain_mask``

**Distribution of extent**

From top to bottom:
- The duration of the ATR measurement related to the individual clouds and cloud clusters.
- The horizontal extent of the clouds and cloud clusters.
- The vertical extent of the clouds and cloud clusters.

<img src="{{"assets/images/compare_cluster_and_clouds/all_altitudes/extent_distribution_rain_mask.png", | relative_url}}" alt="extent_distribution_rain_mask" width="66%"/>

It can be seen, that the number of identified cloud clusters is much low that these of clouds

**Distribution of altitude** 

Please be aware, that this is not the real altitude of all clouds during EUREC4A, but the hwight, at which the ATR aircraft flew through a cloud which was identified in the resulting dataset.
The strong presence of cloud below 1500m is due to the mission of the ATR to capture cloud base properties and thus it's low flight altitude.

<img src="{{"assets/images/compare_cluster_and_clouds/all_altitudes/altitude_distribution_rain_mask.png", | relative_url}}" alt="altitude_distribution_rain_mask" width="66%"/>



### Comparison of ``rain_mask`` and ``cloud_mask``

As the ``cloud_composite`` dataset provides multiple mask, the identified clouds and cloud clusters can differ.
In the table below, the same figures as above can be seen but for two different ``masks``: ``rain_mask`` and ``cloud_mask``.

| Distribution of: |``rain_mask``|``cloud_mask``|
| -  | - | - |
|**Extent**|![Image]({{"assets/images/compare_cluster_and_clouds/all_altitudes/extent_distribution_rain_mask.png", | relative_url }})|![Image]({{"assets/images/compare_cluster_and_clouds/all_altitudes/extent_distribution_cloud_mask.png", | relative_url }})|
|**Altitude**|![Image]({{"assets/images/compare_cluster_and_clouds/all_altitudes/altitude_distribution_rain_mask.png", | relative_url }})|![Image]({{"assets/images/compare_cluster_and_clouds/all_altitudes/altitude_distribution_cloud_mask.png", | relative_url }})|

**Footnotes**

[^1]: The term *Cloud clusters* as mentioned here is used a bit different from in the litearture. Here it refers to a union of small and even large clouds along the ATR flight path, if they are only seperated by a small cloud hole.
