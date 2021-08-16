# foundcog_adult_pilot_volumetric

## Volumetric processing for the foundcog-adult-pilot-2 data
* Downloads data in bids format from s3
* Removes skull from anatomical image using fsl bet 
* Calculates motion correction of each functional series using fsl mcflirt
* Runs registration following these steps - all using fsl flirt:
  * Registration of anatomical T1 on functional images (for each task)
  * Registration of fsl/MNI152_T1_1mm_brain.nii.gz on anatomical T1 (previously registered on func) and saving of output transformation matrix
  * Registration of Schaefer atlas on native space by appliying the previouslty saved transformation matrix 
  
  **It was not possible to register functional images on T1 images because of lack of RAM space.
    It was not possible to easily use directly the volumetric preprocessed images from fmriprep because they use an outdated MNI space which does not match FSL's MNI space, 
    and, hence, Scheafer's atlas space. A Schaefer's atlas in fmriprep MNI space is available from Oxford in datalad structure if for the future we'd rather use that.**
  
* Exctract timecourses for each ROI using ANTS 3dROIstats function (from terminal because of naming mismatch in nipype of the option numROI)
