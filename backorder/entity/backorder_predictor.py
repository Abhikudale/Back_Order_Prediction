import os
import sys

from backorder.exception import BackOrderException
from backorder.util.util import load_object

import pandas as pd


class BackOrderData:

    def __init__(self,
                sku: float,
                national_inv: float,
                lead_time: float,
                in_transit_qty: float,
                forecast_3_month: float,
                forecast_6_month: float,
                forecast_9_month: float,
                sales_1_month: float,
                sales_3_month: float,
                sales_6_month: float,
                sales_9_month: float,
                min_bank: float,
                pieces_past_due: float,
                perf_6_month_avg: float,
                perf_12_month_avg: float,
                local_bo_qty: float,
                deck_risk: str,
                oe_constraint: str,
                ppap_risk: str,
                stop_auto_buy: str,
                rev_stop: str,
                potential_issue: str,
                went_on_backorder: str = None
                 ):
        try:
            self.sku = sku,
            self.national_inv = national_inv,
            self.lead_time = lead_time,
            self.in_transit_qty = in_transit_qty,
            self.forecast_3_month = forecast_3_month,
            self.forecast_6_month = forecast_3_month,
            self.forecast_9_month = forecast_9_month,
            self.sales_1_month = sales_1_month,
            self.sales_3_month = sales_3_month,
            self.sales_6_month = sales_6_month,
            self.sales_9_month = sales_9_month,
            self.min_bank = min_bank,
            self.pieces_past_due = pieces_past_due,
            self.perf_6_month_avg = perf_6_month_avg,
            self.perf_12_month_avg = perf_12_month_avg,
            self.local_bo_qty = local_bo_qty,
            self.deck_risk = deck_risk,
            self.oe_constraint = oe_constraint,
            self.ppap_risk = ppap_risk,
            self.stop_auto_buy = stop_auto_buy,
            self.rev_stop = rev_stop,
            self.potential_issue = potential_issue,
            self.went_on_backorder = went_on_backorder
            
        except Exception as e:
            raise BackOrderException(e, sys) from e

    def get_backorder_input_data_frame(self):

        try:
            backorder_input_dict = self.get_backorder_data_as_dict()
            return pd.DataFrame(backorder_input_dict)
        except Exception as e:
            raise BackOrderException(e, sys) from e

    def get_backorder_data_as_dict(self):
        try:
            input_data = {
                "sku":[self.sku],
                "national_inv":[self.national_inv],
                "lead_time":[self.lead_time],
                "in_transit_qty":[self.in_transit_qty],
                "forecast_3_month":[self.forecast_3_month],
                "forecast_3_month":[self.forecast_6_month],
                "forecast_9_month":[self.forecast_9_month],
                "sales_1_month":[self.sales_1_month],
                "sales_3_month":[self.sales_3_month],
                "sales_6_month":[self.sales_6_month],
                "sales_9_month":[self.sales_9_month],
                "min_bank":[self.min_bank],
                "pieces_past_due":[self.pieces_past_due],
                "perf_6_month_avg":[self.perf_6_month_avg],
                "perf_12_month_avg":[self.perf_12_month_avg],
                "local_bo_qty":[self.local_bo_qty],
                "deck_risk":[self.deck_risk],
                "oe_constraint":[self.oe_constraint],
                "ppap_risk":[self.ppap_risk],
                "stop_auto_buy":[self.stop_auto_buy],
                "rev_stop":[self.rev_stop],
                "potential_issue":[self.potential_issue],
                "went_on_backorder": [self.went_on_backorder]
                }
            return input_data
        except Exception as e:
            raise BackOrderException(e, sys)


class BackOrderPredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise BackOrderException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise BackOrderException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            median_house_value = model.predict(X)
            return median_house_value[0]
        except Exception as e:
            raise BackOrderException(e, sys) from e