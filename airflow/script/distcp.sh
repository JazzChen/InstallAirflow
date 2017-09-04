hadoop distcp  hdfs://192.168.102.11:8020/user/hive/warehouse/source_data.db/t_rules_engine         hdfs://nameservice1/user/hive/warehouse/source_data.db/t_rules_engine
hadoop distcp  hdfs://192.168.102.11:8020/user/hive/warehouse/source_data.db/t_rules_engine_uniq    hdfs://nameservice1/user/hive/warehouse/source_data.db/t_rules_engine_uniq
hadoop distcp  hdfs://192.168.102.11:8020/user/hive/warehouse/source_data.db/t_rules_engine_parquet hdfs://nameservice1/user/hive/warehouse/source_data.db/t_rules_engine_parquet

hive -e "msck repair table source_data.t_rules_engine         ;
         msck repair table source_data.t_rules_engine_uniq    ;
         msck repair table source_data.t_rules_engine_parquet ;"
