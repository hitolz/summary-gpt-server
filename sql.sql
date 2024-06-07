DROP TABLE IF EXISTS `article_cache`;
CREATE TABLE `article_cache` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文章链接',
  `summary_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '摘要内容',
  `active` tinyint(1) DEFAULT '1' COMMENT '记录是否有效(1有效，0无效)，逻辑删除标识',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `expire_time` datetime DEFAULT NULL COMMENT '过期时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `auth_site`;
CREATE TABLE `auth_site` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_id` bigint NOT NULL COMMENT '用户id',
  `site_domain` varchar(100) NOT NULL COMMENT '网站域名',
  `site_summary_key` varchar(10) DEFAULT NULL COMMENT '网站对应的key',
  `active` tinyint(1) DEFAULT '1' COMMENT '记录是否有效(1有效，0无效)，逻辑删除标识',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `expire_hours` int DEFAULT '1000',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `account` varchar(20) NOT NULL COMMENT '账号/登录名',
  `password` varchar(20) NOT NULL COMMENT '密码',
  `tokens` bigint DEFAULT NULL COMMENT '剩余tokens',
  `summary_key` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '后台生成的唯一key',
  `openai_key` varchar(52) DEFAULT NULL COMMENT 'openai key',
  `active` tinyint(1) DEFAULT '1' COMMENT '记录是否有效(1有效，0无效)，逻辑删除标识',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

