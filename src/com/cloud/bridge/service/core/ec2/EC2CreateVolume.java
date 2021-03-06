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
package com.cloud.bridge.service.core.ec2;

import org.apache.log4j.Logger;

import com.cloud.bridge.service.exception.EC2ServiceException;


public class EC2CreateVolume {
    protected final static Logger logger = Logger.getLogger(EC2CreateVolume.class);

	private int    size;   // <- in gigs
	private String snapshotId;
	private String zoneName;
    
	public EC2CreateVolume() {
		size       = 0;
		snapshotId = null;
		zoneName   = null;
	}
	
	/**
	 * Define the size of the volume to create
	 * 
	 * @param size - valid values are [1 .. 1024] and represent gigBytes
	 */
	public void setSize( String size ) {
		try {
		    this.size = Integer.parseInt( size );
		}
		catch( NumberFormatException e ) {
			logger.error( "Bad volume Size parameter: " + e.toString());
			throw new EC2ServiceException( "Bad volume size parameter: " + size + ", expecting [1..1024]", 400 );
		}
		
		if (!(1 <= this.size && 1024 >= this.size))
			throw new EC2ServiceException( "Bad volume size parameter: " + size + ", expecting [1..1024]", 400 );
	}
	
	public int getSize() {
		return this.size;
	}

	public void setSnapshotId( String snapshotId ) {
		this.snapshotId = snapshotId;
	}
	
	public String getSnapshotId() {
		return this.snapshotId;
	}

	public void setZoneName( String zoneName ) {
		this.zoneName = zoneName;
	}
	
	public String getZoneName() {
		return this.zoneName;
	}
}
