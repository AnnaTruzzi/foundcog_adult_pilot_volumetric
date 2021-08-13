
import os
import numpy as np 
import boto3
import pandas as pd 
from nipype.interfaces import fsl
from nipype.interfaces.ants import Registration
from nipype.utils.filemanip import Path
from nipype.interfaces.ants import ApplyTransforms
from nipype.interfaces import afni as afni

s3=boto3.client('s3')
bucket='foundcog-adult-pilot'
sub_list = ['sub-03']

#tasks_list = ['resting_run-1', 'video_run-1', 'video_run-2']
tasks_list = ['resting_run-1']
count = 1

for sub in sub_list:
    for task in tasks_list :
        temp_pth = '/home/annatruzzi/foundcog_adult_pilot_volumetric/temp/'
        s3.download_file(bucket, f'foundcog-adult-pilot-2/deriv-2_topup/fmriprep/{sub}/ses-001/func/{sub}_ses-001_task-{task}_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz', f'{sub}_ses-001_task-{task}_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz')
        s3.download_file(bucket, f'foundcog-adult-pilot-2/deriv-2_topup/fmriprep/{sub}/ses-001/func/{sub}_ses-001_task-{task}_from-T1w_to-scanner_mode-image_xfm.txt', f'{sub}_ses-001_task-{task}_from-T1w_to-scanner_mode-image_xfm.txt')
        os.system(f'mv {sub}_ses-001_task-{task}_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz ../temp/')
        os.system(f'mv {sub}_ses-001_task-{task}_from-T1w_to-scanner_mode-image_xfm.txt ../temp/')

        if count == 0:
            ## Register atlas to pilot space
            print('Registering FSL MNI to pilot space')
            regflt = fsl.FLIRT()
            regflt.inputs.in_file = Path('/dhcp/rhodri_registration/atlases/schaefer/Parcellations/MNI/Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm.nii.gz')
            regflt.inputs.reference = os.path.join(temp_pth, f'{sub}_ses-001_run-1_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz')
            regflt.inputs.out_file = os.path.join(temp_pth, 'FSLMNI_to_MNI152NLin2009cAsym.nii.gz')
            regflt.inputs.out_matrix_file = os.path.join(temp_pth, f'{sub}_ses-001_template_to_native.mat')
            res = regflt.run()

            print('Registering FSL MNI to pilot space')
            regflt = fsl.FLIRT()
            regflt.inputs.in_file = Path('/dhcp/rhodri_registration/atlases/schaefer/Parcellations/MNI/Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm.nii.gz')
            regflt.inputs.reference = os.path.join(temp_pth, f'{sub}_ses-001_run-1_space-_desc-brain_mask.nii.gz')
            regflt.inputs.out_file = os.path.join(temp_pth, 'FSLMNI_to_MNI152NLin2009cAsym.nii.gz')
            regflt.inputs.out_matrix_file = os.path.join(temp_pth, f'{sub}_ses-001_template_to_native.mat')
            res = regflt.run()

        #os.system('invwarp -r ../temp/{sub}_ses-001_task-{task}_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz -w  -o')
        #print(f'{sub} {task} - Working on applywarp...')
        #os.system(f'fslascii2img ../temp/{sub}_ses-001_task-{task}_from-T1w_to-scanner_mode-image_xfm.txt')
        #os.system(f'applywarp -i /dhcp/rhodri_registration/atlases/schaefer/Parcellations/MNI/Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm.nii.gz -o ../temp/{sub}_{task}_Schaefer_resliced.nii.gz -r ../temp/{sub}_ses-001_task-{task}_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz -w ../temp/{sub}_ses-001_task-{task}_from-T1w_to-scanner_mode-image_xfm.nii.gz')
        #print(f'{sub} {task} - Extracting timecourses...')
        #os.system(f'3dROIstats -mask_f2short -mask ../temp/{sub}_{task}_Schaefer_resliced.nii.gz -nomeanout -numROI 400 -quiet -nzmean /home/annatruzzi/foundcog_adult_pilot_volumetric/temp/{sub}_ses-001_task-{task}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz > /home/annatruzzi/foundcog_adult_pilot_volumetric/temp/{sub}_ses-001_task-{task}_Schaefer400_timecourses.txt')

        os.system(f'fslmeants -i ../temp/{sub}_ses-001_task-{task}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz --label=tpl-MNI152NLin2009cAsym_res-01_atlas-Schaefer2018_desc-400Parcels17Networks_dseg.nii.gz -o ../temp/{sub}_ses-001_task-{task}_Schaefer400_timecourses.txt')
        #s3.upload_file(os.path.join(temp_pth, f'{sub}_{task}_Schaefer_resliced.nii.gz'), bucket, f'foundcog-adult-pilot-2/volumetric-timecourses/{sub}/{sub}_{task}_Schaefer_resliced.nii.gz')
        s3.upload_file(os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_Schaefer400_timecourses.txt'), bucket, f'foundcog-adult-pilot-2/volumetric-timecourses/{sub}/{sub}_ses-001_task-{task}_Schaefer400_timecourses.txt')



        ## Extract timecourses with FSL
        #print(f'Extracting timecourses - {sub} {task}')
        #roifsl = fsl.ImageMeants()
        #roifsl.inputs.in_file = os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz')
#        roifsl.inputs.mask = Path('/dhcp/rhodri_registration/atlases/schaefer/Parcellations/MNI/Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm.nii.gz')
        #roifsl.inputs.label = Path(os.path.join(temp_pth, 'Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm_resliced.nii.gz'))
        #roifsl.inputs.out_file = os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_Schaefer400_timecourses.txt')
        #print(roifsl.cmdline)
        #res = roifsl.run()
        #s3.upload_file(os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_Schaefer400_timecourses.txt'), bucket, f'foundcog-adult-pilot-2/volumetric-timecourses/{sub}/{sub}_ses-001_task-{task}_Schaefer400_timecourses.txt')


        ## Extract timecourses with AFNI
        #print(f'Extracting timecourses - {sub} {task}')
        #roistats = afni.ROIStats()
        #roistats.inputs.in_file = os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz')
        #roistats.inputs.mask_file = Path('/dhcp/rhodri_registration/atlases/schaefer/Parcellations/MNI/Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm.nii.gz')
        #roistats.inputs.quiet=True
        #roistats.inputs.mask_f2short = True
        #roistats.inputs.num_ROI = 400
        #roistats.inputs.nomeanout = True
        #roistats.inputs.stat = ['mean']
        #roistats.inputs.out_file = os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_Schaefer400_timecourses.txt')
        #print(roistats.cmdline)
        #res = roistats.run()
        
        #os.system('3dROIstats -mask_f2short -mask /dhcp/rhodri_registration/atlases/schaefer/Parcellations/MNI/Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm.nii.gz -nomeanout -numROI 400 -quiet -nzmean /home/annatruzzi/foundcog_adult_pilot_volumetric/temp/sub-02_ses-001_task-resting_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz > /home/annatruzzi/foundcog_adult_pilot_volumetric/temp/sub-02_ses-001_task-resting_run-1_Schaefer400_timecourses.txt')
        
        
        ###################
        # TENTATIVE STEPS #
        ###################
        '''s3.download_file(bucket, f'foundcog-adult-pilot-2/bids/{sub}/ses-001/func/{sub}_ses-001_task-{task}_bold.nii.gz', f'{sub}_ses-001_task-{task}_bold.nii.gz')
        s3.download_file(bucket, f'foundcog-adult-pilot-2/bids/{sub}/ses-001/anat/{sub}_ses-001_run-001_T1w.nii.gz', f'{sub}_ses-001_run-001_T1w.nii.gz')
        os.system(f'mv {sub}_ses-001_task-{task}_bold.nii.gz ../temp/')
        os.system(f'mv {sub}_ses-001_run-001_T1w.nii.gz ../temp/')
        
        ## Skull stripping 
        print(f'{sub} - Working on bet...')
        btr = fsl.BET()
        btr.inputs.in_file = Path(os.path.join(temp_pth, f'{sub}_ses-001_run-001_T1w.nii.gz'))
        btr.inputs.frac = 0.5
        btr.inputs.out_file = os.path.join(temp_pth, f'{sub}_ses-001_T1w_bet.nii.gz')
        #res = btr.run()
        #s3.upload_file(os.path.join(temp_pth, f'{sub}_ses-001_T1w_bet.nii.gz'), bucket, f'foundcog-adult-pilot-2/volumetric_preprocessing/bet/{sub}/{sub}_ses-001_T1w_bet.nii.gz')

        ## Motion correction
        print(f'{sub} - Working on motion correction...')
        mcflt = fsl.MCFLIRT()
        mcflt.inputs.in_file= Path(os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_bold.nii.gz'))
        mcflt.inputs.cost='mutualinfo'
        mcflt.inputs.output_type = 'NIFTI_GZ'
        mcflt.inputs.out_file = os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_bold_mcflirt.nii.gz')
        mcflt.inputs.save_plots = True
        #res = mcflt.run()
        #s3.upload_file(os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_bold_mcflirt.nii.gz'), bucket, f'foundcog-adult-pilot-2/volumetric_preprocessing/motion-correction/{sub}/{sub}_ses-001_task-{task}_bold_mcflirt.nii.gz')
        #s3.upload_file(os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_bold_mcflirt.nii.gz.par'), bucket, f'foundcog-adult-pilot-2/volumetric_preprocessing/motion-correction/{sub}/{sub}_ses-001_task-{task}_bold_mcflirt.nii.gz.par')

        ## T1-Coregistration
        print(f'{sub} - Working on registration...')
        flt = fsl.FLIRT(bins=640, cost_func='mutualinfo')
        flt.inputs.in_file = os.path.join(temp_pth, f'{sub}_ses-001_T1w_bet.nii.gz')
        flt.inputs.reference = Path('/dhcp/rhodri_registration/atlases/fsl/MNI152_T1_1mm_brain.nii.gz')
        flt.inputs.output_type = "NIFTI_GZ"
        flt.inputs.out_file = os.path.join(temp_pth, f'{sub}_ses-001_T1w_RegisteredToMNI.nii.gz')
        flt.inputs.out_matrix_file = os.path.join(temp_pth, f'{sub}_ses-001_transform.mat')
        #res = flt.run()

        print(f'{sub} - Working on functional registration...')
        flt_func = fsl.FLIRT()
        flt_func.inputs.in_file = Path(os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_bold_mcflirt.nii.gz'))
        flt_func.inputs.reference = os.path.join(temp_pth, f'{sub}_ses-001_T1w_RegisteredToMNI.nii.gz')
        flt_func.inputs.apply_xfm = True
        flt_func.inputs.in_matrix_file = os.path.join(temp_pth, f'{sub}_ses-001_transform.mat')
        flt_func.inputs.output_type = "NIFTI_GZ"
        flt_func.inputs.out_file = os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_bold_RegisteredToMNI.nii.gz')
        res = flt_func.run()
        s3.upload_file(os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_bold_RegisteredToMNI.nii.gz'), bucket, f'foundcog-adult-pilot-2/volumetric_preprocessing/t1-coregistration/{sub}/{sub}_ses-001_task-{task}_bold_RegisteredToMNI.nii.gz')
        s3.upload_file(os.path.join(temp_pth, f'{sub}_ses-001_transform.mat'), bucket, f'foundcog-adult-pilot-2/volumetric_preprocessing/t1-coregistration/{sub}/{sub}_ses-001_transform.nii.gz')
        s3.upload_file(os.path.join(temp_pth, f'{sub}_ses-001_T1w_RegisteredToMNI.nii.gz'), bucket, f'foundcog-adult-pilot-2/volumetric_preprocessing/t1-coregistration/{sub}/{sub}_ses-001_T1w_RegisteredToMNI.nii.gz')
        '''

        
        #### ANTS registration
        '''reg = Registration()
        reg.inputs.fixed_image = Path('/dhcp/rhodri_registration/atlases/fsl/MNI152_T1_1mm_brain.nii.gz')
        reg.inputs.moving_image = os.path.join(temp_pth, f'{sub}_ses-001_T1w_bet.nii.gz')
        #reg.inputs.interpolation = 'NearestNeighbor'
        reg.inputs.metric = ['Mattes']*2
        reg.inputs.metric_weight = [1]*2 # Default (value ignored currently by ANTs)
        reg.inputs.shrink_factors = [[2,1], [3,2,1]]
        reg.inputs.smoothing_sigmas = [[1,0], [2,1,0]]
        reg.inputs.transforms = ['Affine']
        reg.inputs.number_of_iterations = [[1500, 200], [100, 50, 30]]
        reg.inputs.output_warped_image = os.path.join(temp_pth, f'{sub}_ses-001_T1w_warped.nii.gz')
        reg.inputs.transform_parameters = [(2.0,)]
        #reg.inputs.dimension = 3
        #reg.inputs.save_state = os.path.join(temp_pth, f'{sub}_ses-001_run-001_')
        reg.inputs.output_inverse_warped_image = os.path.join(temp_pth, f'{sub}_ses-001_T1w_Inversewarped.nii.gz')
        res = reg.run()
        os.system('mv transform0GenericAffine.mat  ../temp/')

        at = ApplyTransforms()
        at.inputs.input_image = Path(os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_bold_mcflirt.nii.gz'))
        at.inputs.reference_image = os.path.join(temp_pth, f'{sub}_ses-001_T1w_bet.nii.gz')
        at.inputs.transforms = [os.path.join(temp_pth,'transform0GenericAffine.mat'), os.path.join(temp_pth, f'{sub}_ses-001_T1w_Inversewarped.nii.gz')]
        at.inputs.interpolation = 'NearestNeighbor'
        at.inputs.invert_transform_flags = [True, False]
        at.inputs.output_image = os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_bold_RegisteredToMNI.nii.gz')
        res = at.run()
        s3.upload_file(os.path.join(temp_pth, f'{sub}_ses-001_task-{task}_bold_RegisteredToMNI.nii.gz'), bucket, f'foundcog-adult-pilot-2/volumetric_preprocessing/t1-coregistration/{sub}/{sub}_ses-001_task-{task}_bold_RegisteredToMNI.nii.gz')
        s3.upload_file(os.path.join(temp_pth, f'{sub}_ses-001_T1w_Inversewarped.nii.gz'), bucket, f'foundcog-adult-pilot-2/volumetric_preprocessing/t1-coregistration/{sub}/{sub}_ses-001_T1w_Inversewarped.nii.gz')
        s3.upload_file(os.path.join(temp_pth, f'{sub}_ses-001_T1w_warped.nii.gz'), bucket, f'foundcog-adult-pilot-2/volumetric_preprocessing/t1-coregistration/{sub}/{sub}_ses-001_T1w_warped.nii.gz')
        s3.upload_file(os.path.join(temp_pth, f'transform0GenericAffine.mat'), bucket, f'foundcog-adult-pilot-2/volumetric_preprocessing/t1-coregistration/{sub}/transform0GenericAffine.mat')
        '''

        ## Extract timecourses



        a = 1



