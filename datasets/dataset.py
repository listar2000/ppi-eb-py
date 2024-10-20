"""
Base class for a generic dataset class. A dataset in PPI-EB project takes care of:
- Loading logic for the dataset
- Storing metadata information
- (If required) Computing predictions for unlabelled data
"""
import numpy as np

class PPIEmpBayesDataset(object):
    def __init__(self, dataset_name: str, verbose: bool = False):
        self.dataset_name = dataset_name
        self.verbose = verbose

        pred_labelled, y_labelled, pred_unlabelled, y_unlabelled, true_theta = self.load_data()

        self.validate_data(pred_labelled, y_labelled, pred_unlabelled, y_unlabelled)
        
        self.pred_labelled: list[np.ndarray] = pred_labelled
        self.y_labelled: list[np.ndarray] = y_labelled
        self.pred_unlabelled: list[np.ndarray] = pred_unlabelled
        self.y_unlabelled: list[np.ndarray] = y_unlabelled
        self.true_theta: np.ndarray = true_theta

        self.M: int = len(pred_labelled)  # number of problems
        self.ns: np.ndarray = np.array([x.shape[0] for x in pred_labelled])  # number of labelled samples for each problem
        self.Ns: np.ndarray = np.array([x.shape[0] for x in pred_unlabelled])  # number of unlabelled samples for each problem

    def load_data(self) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray], list[np.ndarray], np.ndarray]:
        raise NotImplementedError("Subclasses must implement this method")
    
    def validate_data(self, x_labelled: list[np.ndarray], 
                      y_labelled: list[np.ndarray], 
                      x_unlabelled: list[np.ndarray], 
                      y_unlabelled: list[np.ndarray]) -> None:
        assert len(x_labelled) == len(y_labelled) == len(x_unlabelled) == len(y_unlabelled), "Mismatch in number of problems"

        for i in range(len(x_labelled)):
            assert x_labelled[i].shape[0] == y_labelled[i].shape[0], f"Mismatch in number of labelled samples for problem {i}"
            assert x_unlabelled[i].shape[0] == y_unlabelled[i].shape[0], f"Mismatch in number of unlabelled samples for problem {i}"
            assert np.isnan(x_labelled[i]).sum() == 0, f"NaNs found in labelled pred for problem {i}"
            assert np.isnan(y_labelled[i]).sum() == 0, f"NaNs found in labelled y for problem {i}"
            assert np.isnan(x_unlabelled[i]).sum() == 0, f"NaNs found in unlabelled pred for problem {i}"
            assert np.isnan(y_unlabelled[i]).sum() == 0, f"NaNs found in unlabelled y for problem {i}"
        
        if self.verbose:
            print(f"Data validation successful for `{self.dataset_name}`")

