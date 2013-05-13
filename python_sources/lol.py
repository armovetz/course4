import cross_validation
import engine
import svd
import content_based
import estimate
import reporter
#import prepare_matrices
#prepare_matrices.fullPrepares(False)
#prepare_matrices.fullPrepares(True)

time_flag = True
prediction_flag = True
estimate_flag = True

# FUNCTION TO RIDE
prediction_file_name = "prediction_cb.mtx"
results_file_name = "results_cb"
prediction_function = content_based.prediction
estimate_function = estimate.estimateNDCGp

# REPORT
report_file = reporter.reporter(prediction_function, prediction_flag, prediction_file_name, estimate_function, estimate_flag, results_file_name, time_flag)

#cross_validation.launchCrossValidation(prediction_function, prediction_flag, time_flag, estimate_flag, prediction_file_name, results_file_name)
cross_validation.launchCrossValidation(prediction_function, prediction_flag, prediction_file_name, \
    estimate_function, estimate_flag, results_file_name, \
    time_flag, report_file)

#cross_validation.launchDebugCase(prediction_function, prediction_flag, prediction_file_name, estimate_function, estimate_flag, results_file_name, "../data/tmp/cross_validation/2_3")
#cross_validation.launchDebugCase(prediction_function, True, True, prediction_file_name, results_file_name, "../data/tmp/diag_cross_validation/1")
#cross_validation.launchDebugCase(prediction_function, True, True, prediction_file_name, results_file_name, "../data/tmp/diag_cross_validation/2")
#cross_validation.launchDebugCase(prediction_function, True, True, prediction_file_name, results_file_name, "../data/tmp/diag_cross_validation/3")
#cross_validation.launchDebugCase(prediction_function, True, True, prediction_file_name, results_file_name, "../data/tmp/diag_cross_validation/4")

#cross_validation.launchCase(engine.prediction, True, False, False, "prediction_engine.mtx", "results_engine", "4_0")
#cross_validation.launchCase(engine.prediction, True, False, False, "prediction_engine.mtx", "results_engine", "4_1")
#cross_validation.launchCase(engine.prediction, True, False, False, "prediction_engine.mtx", "results_engine", "4_2")
#cross_validation.launchCase(engine.prediction, True, False, False, "prediction_engine.mtx", "results_engine", "4_3")
#cross_validation.launchCase(engine.prediction, True, False, False, "prediction_engine.mtx", "results_engine", "4_4")





