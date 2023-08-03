"""Script that controls the LED to display whether timestamp matches displayed data."""

from org.csstudio.opibuilder.scriptUtil import PVUtil

# pvs[0]: loc://$(DID)_time_led_{device_type}
# pvs[1]: loc://$(DID)_time_{device_type}
# pvs[2]: loc://$(DID)_trigger_time_led_{device_type}(0)
# pvs[3]: loc://$(DID)_old_timestamp_{device_type}
# pvs[4]: loc://$(DID)_time_travel_{device_type}
# pvs[5]: loc://$(DID)_debug_message_{device_type}

# The trigger has been updated
current_timestamp = PVUtil.getString(pvs[1])
saved_timestamp = PVUtil.getString(pvs[3])

# If the timestamp matches the saved one, turn LED on
if saved_timestamp == current_timestamp:
    if PVUtil.getDouble(pvs[4]) == 1:
        pvs[0].setValue(1)

# If the timestamp is different, turn LED off and update the saved timestamp
else:
    if PVUtil.getDouble(pvs[4]) == 1:
        pvs[0].setValue(0)
        pvs[3].setValue(current_timestamp)
    pvs[5].setValue('WARNING: Timestamp does not match time travel data!')
