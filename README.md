# Exporter
Exporting blender files very fast as a demo render or master export in my pipeline.

**Install just the .py file as an addon and dont be stupid about it**

The N menu has a button, the dialog popup allows you to choose wheter you want to save incrementally before making a sweatbox video.
If you are like me and don't like buttons, you can type in F3 and click `pipeline.demo_exporter_dialog > *Demo Exporter*` instead!

folder structure:

`Task/Shotnumber/tyPe/Content`

>Task
>>001.00_asset
>>>001.00_asset.mp4 (created file based on latest version of the file inside Demo)
>>>
>>>Source
>>>>001.00_asset_001.blend
>>>>
>>>Demo
>>>>001.00_asset_001.mp4 (created file)
