import pandas as pd 
import datetime as dt 
from . import config
from tsalchemy.tsalchemy import ts_tools
from tsalchemy.tsalchemy.single_factor_dfm import SingleFactorDFM
from wd.wd_api import wdAPI

class IndexModel:
	"""动态因子模型类，用于生成宏观经济指数"""
	
	def __init__(self, index_name, s_ref=None, bng_date=None, end_date=None, env_var_name=None, 
												user_config_path=None, system_config_path=None):
		"""初始化模型
		"""
		if bng_date is None:
			bng_date = '2000-01-01'
		if end_date is None:
			end_date = dt.datetime.now().strftime('%Y-%m-%d')
		self.bng_date = bng_date
		self.end_date = end_date
		self.indicators_config = config.parse_config(env_var_name, user_config_path, system_config_path)
		self.wd_api = None 
		self.raw_data = {}
		self.yoy_data = {}
		self.stl_data = {}
		self.index_name = index_name
		self.s_ref = s_ref
		self.dfm = None

	def build_model(self):
		"""构建模型"""
		self.fetch_data()
		self.process_data()
		self.generate_index()
		
	def fetch_data(self):
		"""从Wind获取宏观经济指标数据"""
		self.wd_api = wdAPI()
		for wd_code in self.indicators_config.keys():
			error_code, df = self.wd_api.w.edb(wd_code, self.bng_date, self.end_date, usedf=True)
			if error_code != 0:
				raise ValueError(f"Error fetching data for {wd_code}: {error.message}")
			df.columns = [self.indicators_config[wd_code]['name']]
			df.index = pd.to_datetime(df.index)
			self.raw_data[wd_code] = df

	def transform_ts_to_yoy(self, wd_code):
		"""将时间序列转换为同比"""
		wd_name = self.indicators_config[wd_code]['name']
		ts_type = self.indicators_config[wd_code]['indicator_type']
		ts_raw = self.raw_data[wd_code][wd_name]
		if ts_type in ['当期值', '年累计值']:
			ts_yoy = ts_tools.current_to_yoy(ts_raw)
		elif ts_type == '环比值':
			ts_index = ts_tools.ror_to_index(ts_raw)
			ts_yoy = ts_tools.current_to_yoy(ts_index)
		else:
			raise ValueError(f"Unsupported indicator type: {ts_type}")
		self.yoy_data[wd_code] = ts_yoy

	def stl_decomposition(self, wd_code):
		wd_name = self.indicators_config[wd_code]['name']
		stl_component = self.indicators_config[wd_code]['stl']
		ts_yoy = self.yoy_data[wd_code]
		if ts_yoy.isna().sum() > 0:
			freq = ts_tools.infer_frequency(ts_yoy.index)
			ts_yoy = ts_yoy.dropna().resample(freq).last().interpolate()
		ts_stl = ts_tools.get_stl_components(ts_yoy, components=stl_component)
		self.stl_data[wd_code] = ts_stl
	
	def process_data(self):
		"""处理原始数据，包括清洗、标准化等"""
		for wd_code in self.indicators_config.keys():
			self.transform_ts_to_yoy(wd_code)
			self.stl_decomposition(wd_code)
	
	def generate_index(self):
		"""运行动态因子模型，生成宏观经济指数"""
		df_input = pd.DataFrame(self.stl_data)
		df_input.columns = [self.indicators_config[wd_code]['name'] for wd_code in self.indicators_config.keys()]
		df_input.index = pd.to_datetime(df_input.index)
		dfm = SingleFactorDFM(df_input, s_ref=self.s_ref, factor_name=self.index_name)
		dfm.build_model()	
		self.dfm = dfm 
