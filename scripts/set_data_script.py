"""Script that is run when PVs are being set to historic data."""

from org.csstudio.opibuilder.scriptUtil import PVUtil

# pvs[0]: loc://$(DID)_trigger_time_set_{device_type}
# pvs[1]: loc://$(DID)_debug_message_{device_type}
# pvs[2]: loc://$(DID)_time_travel_{device_type}

# Index at which VA PVs actually start
PV_START = 3

# Only execute script if in time travel mode
if PVUtil.getDouble(pvs[2]) == 1:
    pvs[1].setValue('Setting data...')

    # Pair up each of the time_travel PVs with their corresponding real PV
    time_travel_pv_list = pvs[PV_START::2]
    real_pv_list = pvs[PV_START + 1::2]

    # Initialize counters
    set_count = 0
    not_set_count = 0

    # Iterate over pairs and set the real PV with the value of the time_travel PV if the conditions
    # are met
    for time_travel_pv, real_pv in zip(time_travel_pv_list, real_pv_list):
        time_travel_value = PVUtil.getString(time_travel_pv)

        # Check conditions to see if we should update the actual PV
        if str(real_pv).endswith("CSET"):
            try:
                real_value = float(time_travel_value)
                real_pv.setValue(real_value)
                set_count += 1

            except ValueError:
                not_set_count += 1
                continue

    # Update the message PV with the final counts
    if set_count > 0:
        pvs[1].setValue('Data set complete. {} PV(s) loaded, {} PV(s) not set.'.format(
            set_count, not_set_count))
    else:
        pvs[1].setValue("No data to set!")
