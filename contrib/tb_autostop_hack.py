    from time import sleep
    last_N, this_N = 0,0
    same_cnt = 0
    while True:
        last_N, this_N = this_N, tb.blocks_file_source_0.nitems_written(0)
        if last_N==this_N:
        	same_cnt += 1
        else:
        	same_cnt = 0
        if same_cnt > 5:
        	break
        sleep(0.5)
    tb.stop()

