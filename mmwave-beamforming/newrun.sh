#bin/bash

# when --cont is set, --epochs has to be higher than the number of epochs executed when the model has been saved the last time (this information is written and retrieved from the weights file name)
# ----------------------------------------------------------------------------------------------------
python -u /home/batool/Directroy/main.py \
> /home/batool/Directroy/log.out \
2> /home/batool/Directroy/log.err
