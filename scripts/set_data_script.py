"""Script that is run when PVs are being set to historic data."""

from org.csstudio.opibuilder.scriptUtil import PVUtil

# Only execute script if in time travel mode
if PVUtil.getDouble(pvs[2]) == 1:
    pass
