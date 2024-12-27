import os
import configparser
from typing import Dict, Any

def get_config_path(env_var_name=None, user_config_path=None, system_config_path=None) -> str:
	"""获取配置文件路径
	
	按以下顺序查找配置文件：
	1. 环境变量 DFM_INDEX_CONFIG 指定的路径
	2. 用户主目录下的 ~/.config/dfm_index_model/macro_indicators.ini
	3. 系统配置目录 /etc/dfm_index_model/macro_indicators.ini
	
	Returns:
		str: 配置文件的完整路径
	
	Raises:
		FileNotFoundError: 当无法找到配置文件时抛出
	"""
	# 1. 首先检查环境变量
	# 例如：DFM_INDEX_CONFIG
	if env_var_name is not None:
		config_path = os.getenv(env_var_name)
		if config_path:
			return config_path
	
	# 2. 检查用户主目录
	# 例如：~/.config/dfm_index_model/macro_indicators.ini
	if user_config_path is not None:
		user_config = os.path.expanduser(user_config_path)
		if os.path.exists(user_config):
			return user_config
	
	# 3. 检查系统配置目录
	# 例如：/etc/dfm_index_model/macro_indicators.ini
	if system_config_path is not None:
		system_config = os.path.expanduser(system_config_path)
		if os.path.exists(system_config):
			return system_config
	
	raise FileNotFoundError("Configuration file not found")

def parse_config(env_var_name=None, user_config_path=None, system_config_path=None) -> Dict[str, Dict[str, Any]]:
	"""解析配置文件，返回字典格式的配置信息
	
	Returns:
		Dict[str, Dict[str, Any]]: 配置信息字典，格式为：
		{
			'S0027012': {
				'name': '产量:发电量',
				'indicator_type': '当期值',
				'dimension': '增长',
				'stl': 'trend'
			},
			...
		}
	
	Raises:
		FileNotFoundError: 配置文件不存在时抛出
		configparser.Error: 配置文件格式错误时抛出
	"""
	config = configparser.ConfigParser()
	config_path = get_config_path(env_var_name, user_config_path, system_config_path)
	config.read(config_path, encoding='utf-8')
	
	# 初始化结果字典
	result = {}
	
	# 遍历所有section
	for section in config.sections():
		# 跳过DEFAULT section
		if section == 'DEFAULT':
			continue
		
		# 获取该section下的所有配置项
		section_dict = dict(config[section])
		
		# 添加到结果字典
		result[section] = {
			'name': section_dict.get('name', ''),
			'indicator_type': section_dict.get('indicator_type', ''),
			'dimension': section_dict.get('dimension', ''),
			'stl': section_dict.get('stl', '')
		}
	
	return result 