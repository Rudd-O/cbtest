/*
 * Copyright 2010 Cloud.com, Inc.
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *      http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.cloud.bridge.service.core.s3;

/**
 * @author Kelven Yang
 */
public class S3ListBucketRequest extends S3Request {
	protected String bucketName;
	protected String prefix;
	protected String marker;
	protected String delimiter;
	protected int maxKeys;

	public S3ListBucketRequest() {
		super();
	}
	
	public String getBucketName() {
		return bucketName;
	}
	
	public void setBucketName(String bucketName) {
		this.bucketName = bucketName;
	}
	
	public String getPrefix() {
		return prefix;
	}
	
	public void setPrefix(String prefix) {
		this.prefix = prefix;
	}
	
	public String getMarker() {
		return marker;
	}
	
	public void setMarker(String marker) {
		this.marker = marker;
	}
	
	public String getDelimiter() {
		return delimiter;
	}
	
	public void setDelimiter(String delimiter) {
		this.delimiter = delimiter;
	}
	
	public int getMaxKeys() {
		return maxKeys;
	}
	
	public void setMaxKeys(int maxKeys) {
		this.maxKeys = maxKeys;
	}
}
