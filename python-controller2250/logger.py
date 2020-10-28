from loguru import logger

logger.add('controller2250.log', **{
    'rotation': '10 MB', 
    'retention': 3,
    'level': 'INFO'
})