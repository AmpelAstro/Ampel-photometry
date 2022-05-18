<img align="left" src="https://desycloud.desy.de/index.php/s/99Jkcyzn92rRpHF/preview" width="150" height="150"/>  
<br>

# Photometry for AMPEL
<br><br>
Vanilla AMPEL treats all `DataPoint` instances the same way (regardless of their properties).
The classes provided in this repository distinguish two types of datapoints: `PhotoPoints` and `UpperLimits`.
By convention, `PhotoPoints` have *positive* ids and `UpperLimits` have *negative* ids.

This add-on introduces new abstract classes, new _views_ and a new T1 _combiner_ class.

The specialized _view_ `LightCurve` comprises a collection of photo points and upper limits together with utility methods to query them. 

T2 units working with photometric data can inherit the abstract class `AbsLightCurveT2Unit` or `AbsTiedLightCurveT2Unit` and 
will then be automatically passed `LightCurve` instances when run. 

Similarily, T3 units inheriting `AbsPhotoT3Unit` will receive `TransientView` instances rather than `SnapView` instances.

The auxiliary filters `PPSFilter` and `ULSFilter` enable the customization of ingestion behavior via the static field _eligible_.
Please see demo units for more info (`DemoFirstPhotoPointT2Unit` for example)
