#ifndef CANHANDLE_H_
#define CANHANDLE_H_
#include "zlgcan.h"

#define INVAILD_CAN_HANDLE (CAN_HANDLE())

struct CAN_HANDLE
{
	CAN_HANDLE()
	{
		this->device_type = 0;
		this->device_index = 0;
		this->channel_index = 0;
	}
	CAN_HANDLE(UINT device_type, UINT device_index, UINT channel_index)
	{
		this->device_type = device_type;
		this->device_index = device_index;
		this->channel_index = channel_index;
	}
	CAN_HANDLE(const DEVICE_HANDLE& device_handle)
	{
		ULONG val = reinterpret_cast<ULONG>(device_handle);
		this->handle = (UINT)val;
	}
	union
	{
		struct
		{
			UINT channel_index:8;
			UINT device_index:8;
			UINT device_type:16;
		};
		UINT handle;
	};
	bool operator==(const CAN_HANDLE& other)
	{
		return this->device_type == other.device_type
			&& this->device_index == other.device_index
			&& this->channel_index == other.channel_index;
	}
	bool operator<(const CAN_HANDLE& other) const
	{
		return handle < other.handle;
	}
	bool IsInvalid()
	{
		return 0 == this->device_type && 0 == this->channel_index && 0 == this->device_index;
	}
};

#endif //CANHANDLE_H_
