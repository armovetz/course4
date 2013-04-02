import prepare_matrices


print "                                *                                "
print "                                                     *           "
print "                           *         00                          "
print "  *                             000000                           "
print "           *                  0000000                            "
print "                            0000000                              "
print "                          00000000                          *    "
print "           *             00000000             *                  "
print "                        000000000                                "
print "                 *      000000000                         *      "
print "   *                    000000000                                "
print "                         000000000           *                   "
print "                           000000000                             "
print "          *                   0000000                     *      "
print "                         *       000000                          "
print "                                     0000                        "
print "           *                               *             *       "
print "                                                                 "
print "      *           *        *                                     "
print "           GOOD NIGHT                               *            "
print "           *                           *                         "
print "GOOD NIGHT!\n"

# create directories for current setting for cross validation
prepare_matrices.prepareDirs()

# create training history matrices for cross validation
prepare_matrices.prepareTrainingMatrices()

# create user_X_meta matrices
prepare_matrices.createUser_x_MetaMatrices()

# create item_X_meta matrix (global)
prepare_matrices.createItem_x_MetaMatrix_global()

# create test history matrices and test clusters
prepare_matrices.prepareTestingMatrices()
