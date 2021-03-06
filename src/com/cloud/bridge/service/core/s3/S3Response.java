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
public class S3Response {
	protected int resultCode;
	protected String resultDescription;
	
	public S3Response() {
	}
	
	public S3Response(int code, String description) {
		resultCode = code;
		resultDescription = description;
	}
	
	public int getResultCode() {
		return resultCode;
	}
	
	public void setResultCode(int code) {
		resultCode = code;
	}
	
	public String getResultDescription() {
		return resultDescription; 
	}
	
	public void setResultDescription(String description) {
		resultDescription = description;
	}
}
