<img align="left" src="https://desycloud.desy.de/index.php/s/99Jkcyzn92rRpHF/preview" width="150" height="150"/>  
<br>

# Photometry for AMPEL
<br><br>
Vanilla AMPEL treats all `DataPoint` instances the same way (regardless of their properties).
The classes provided in this repository distinguish two types of datapoints: `PhotoPoints` and `UpperLimits`.
By convention, `PhotoPoints` have *positive* ids and `UpperLimits` have *negative* ids.


This add-on introduces a new alert subclass, new abstract classes, new _views_ and new T1 and T2 _ingester_ and _compiler_ classes.

`PhotoAlert` is a subclass of `AmpelAlert` that features distinct attributes 
for photopoints and upperlimits, so that filters can query one or the other. 
Further on, specialized _views_ are provided such as `LightCurve`, 
which comprises a collection of photo points and upper limits together with utility methods to query them. 

T2 units working with photometric data can inherit the abstract class `AbsLightCurveT2Unit` and 
will then be automatically passed `LightCurve` instances when run. 

Similarily, T3 units inheriting `AbsPhotoT3Unit` will receive `TransientView` instances rather than `SnapView` instances.

`AbsLightCurveT2Unit` subclasses can influence how ingesters (at the T0 level) 
combine datapoints of an alert together. The static parameter `ingest` determines if 
upper limits are included in compound documents (sometimes referred to as _states_) or not.

<p align="center">
  <img src="https://desycloud.desy.de/index.php/s/z2B3Q2KQw6NDFT6/preview" width="30%" />
  <img src="https://desycloud.desy.de/index.php/s/FZXWMyq3pkeBYft/preview" width="30%" />
  <img src="https://desycloud.desy.de/index.php/s/LnnNzJ4XZyo7QGj/preview" width="30%" /> 
</p>
<p align="center">
  Result of a sequential ingestion of datapoints. <i>Middle</i>: vanilla AMPEL, <i>right</i>: ampel-photometry.</i>
</p>

In the figure above, vanilla AMPEL creates states for `{1, 2}`, `{1, 2, 3}` and  `{1, 2, 3, 4}`.
Using Ampel-photometry, the creation of states and associated T2 document will be dependent on T2 units settings.
If `upper_limits` is True, then the states `{1, 2}` and  `{1, 2, 3, 4}` will be created.
Otherwise, `{1, 2}` and  `{1, 2, 4}` will be created.

This add-on provides T1 and T2 compilers and ingesters capable of handling the complications associated with the introduced options.
Note that specialized classes sometime feature the prefix `Dual` as hint of the datapoint distinctions.
